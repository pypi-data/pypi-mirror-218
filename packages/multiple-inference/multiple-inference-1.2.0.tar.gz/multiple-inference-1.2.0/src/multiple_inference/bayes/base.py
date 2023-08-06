"""Base classes for Bayesian analysis.
"""
from __future__ import annotations

import warnings
from typing import Any, Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import multivariate_normal, norm, rv_continuous, wasserstein_distance

from ..base import ColumnType, ModelBase, Numeric1DArray, ResultsBase, ColumnsType
from ..stats import joint_distribution
from ..utils import weighted_quantile


class BayesResults(ResultsBase):
    """Results of Bayesian analysis.

    Inherits from :class:`multiple_inference.base.ResultsBase`.

    Args:
        *args (Any): Passed to :class:`multiple_inference.base.ResultsBase`.
        n_samples (int): Number of samples used for approximations (ranking, likelihood
            and Wasserstein distance). Defaults to 10000.
        **kwargs (Any): Passed to :class:`multiple_inference.base.ResultsBase`.

    Attributes:
        distributions (List[scipy.stats.norm]): Marginal posterior distributions.
        multivariate_distribution (scipy.stats.multivariate_normal): Joint posterior
            distribution.
        rank_df (pd.DataFrame): (n, n) dataframe of probabilities that column i has
            rank j.
    """

    _default_title = "Bayesian estimates"

    def __init__(self, *args: Any, n_samples: int = 10000, **kwargs: Any):
        super().__init__(*args, **kwargs)

        # get the marginal (posterior) distributions, parameters, and pvalues
        self.marginal_distributions, params, pvalues = [], [], []
        for i in range(self.model.n_params):
            dist = self.model.get_marginal_distribution(i)
            self.marginal_distributions.append(dist)
            params.append(dist.mean())
            pvalues.append(dist.cdf(0))
        self.params = np.array(params).squeeze()
        self.pvalues = np.array(pvalues).squeeze()
        self._n_samples = n_samples
        self._sample_weight = np.full(n_samples, 1 / n_samples)

    @property
    def _posterior_rvs(self):
        if hasattr(self, "_cached_posterior_rvs"):
            return self._cached_posterior_rvs

        # estimate the parameter rankings by drawing from the posterior
        try:
            self.joint_distribution = self.model.get_joint_distribution()
            self._cached_posterior_rvs = self.joint_distribution.rvs(
                size=self._n_samples
            )
        except NotImplementedError:
            warnings.warn(
                "Model does not provide a joint posterior distribution."
                " I'll assume the marginal posterior distributions are independent."
                " Rank estimates and likelihood and Wasserstein approximations may be"
                " unreliable."
            )
            self._cached_posterior_rvs = joint_distribution(
                self.marginal_distributions
            ).rvs(size=self._n_samples)

        return self._cached_posterior_rvs

    @property
    def _reconstructed_rvs(self):
        if hasattr(self, "_cached_reconstructed_rvs"):
            return self._cached_reconstructed_rvs

        self._cached_reconstructed_rvs = np.apply_along_axis(
            lambda mean: multivariate_normal.rvs(mean, self.model.cov),
            1,
            self._posterior_rvs,
        )
        return self._cached_reconstructed_rvs

    @property
    def rank_df(self):
        if hasattr(self, "_cached_rank_df"):
            return self._cached_rank_df

        argsort = np.argsort(-self._posterior_rvs, axis=1)
        rank_matrix = np.array(
            [
                ((argsort == k).T * self._sample_weight).sum(axis=1)
                for k in range(self.model.n_params)
            ]
        ).T
        self._cached_rank_df = pd.DataFrame(
            rank_matrix,
            columns=self.model.exog_names,
            index=np.arange(1, self.model.n_params + 1),
        )
        self._cached_rank_df.index.name = "Rank"
        return self._cached_rank_df

    def compute_best_params(
        self,
        n_best_params: int = 1,
        alpha: float = 0.05,
        superset: bool = True,
        criterion: str = "fwer",
    ) -> pd.Series:
        """Compute the set of best (largest) parameters.

        Args:
            n_best_params (int, optional): Number of best parameters. Defaults to 1.
            alpha (float, optional): Significance level. If the criterion is "fwer",
                alpha is the family-wise error rate. If the criterion is "fdr", alpha is
                the false discovery rate. Defaults to 0.05.
            superset (bool, optional): Indicates that the returned set should be a
                superset of the truly best parameters. If False, the returned set should
                be a subset of the truly best parameters. Defaults to True.
            criterion (str, optional): "fwer" to control the family-wise error rate,
                "fdr" to control the false discovery rate. Defaults to "fwer".

        Raises:
            ValueError: ``criterion`` must be either "fwer" or "fdr".

        Returns:
            pd.Series: Indicates which parameters are in the selected set.
        """
        if criterion not in ("fwer", "fdr"):
            raise ValueError(f"`criterion` must be 'fwer' or 'fdr', got {criterion}.")

        selected_mask = (
            self._compute_best_params_fwer(n_best_params, alpha, superset)
            if criterion == "fwer"
            else self._compute_best_params_fdr(n_best_params, alpha, superset)
        )
        return pd.Series(selected_mask, index=self.exog_names)

    def _compute_best_params_fdr(
        self, n_best_params: int, alpha: float, superset: bool
    ) -> np.ndarray:
        """Compute the set of best parameters controlling the false discovery rate.

        See :meth:`BayesResults.compute_best_params` for arguments.
        """
        if superset:
            pr_in_target = self.rank_df[n_best_params:].sum(axis=0)
        else:
            pr_in_target = self.rank_df[:n_best_params].sum(axis=0)

        fp_rate, selected = 0, []
        while fp_rate < alpha and len(selected) < self.model.n_params:
            selected.append(pr_in_target.argmax())
            fp_rate = (
                (len(selected) - 1) * fp_rate + 1 - pr_in_target[selected[-1]]
            ) / len(selected)
            pr_in_target[selected[-1]] = 0
        selected.pop()
        selected_mask = np.full(self.model.n_params, False)
        selected_mask[selected] = True
        return ~selected_mask if superset else selected_mask

    def _compute_best_params_fwer(
        self, n_best_params: int, alpha: float, superset: bool
    ) -> np.ndarray:
        """Compute the set of best parameters controlling the family-wise error rate.

        See :meth:`BayesResults.compute_best_params` for arguments.
        """
        mask = (-self._posterior_rvs).argsort().argsort() >= n_best_params
        target_n_selected = self.model.n_params - n_best_params
        if superset:
            mask, target_n_selected = ~mask, self.model.n_params - target_n_selected

        selected = []  # selected parameters
        # n_selected is a (n samples,) array where n_selected[i] is the number of
        # selected parameters in the top `n_best_params` for sample i
        n_selected = np.zeros(len(mask))
        # max_n_selected is the maximum number of selected parameters in the top
        # `n_best_params` across samples from the posterior distribution
        max_n_selected = 0

        while (n_selected >= target_n_selected).mean() < 1 - alpha:
            arr = mask[n_selected == min(target_n_selected - 1, max_n_selected)].sum(
                axis=0
            )
            if (arr == 0).all():
                arr = mask[n_selected < target_n_selected].sum(axis=0)
            selected.append(arr.argmax())
            n_selected += mask[:, selected[-1]]
            mask[:, selected[-1]] = False
            max_n_selected += 1

        selected_mask = np.full(self.model.n_params, True)
        selected_mask[selected] = False
        return ~selected_mask if superset else selected_mask

    def rank_conf_int(
        self,
        alpha: float = 0.05,
        columns: ColumnsType = None,
        simultaneous: bool = True,
    ) -> np.ndarray:
        """Compute rank confidence intervals.

        Args:
            alpha (float, optional): Significance level. Defaults to 0.05.
            columns (ColumnsType, optional): Selected columns. Defaults to None.
            simultaneous (bool, optional): Indicates that rank confidence intervals
                should have correct simultaneous coverage. If False, the rank confidence
                intervals will have correct marginal coverage. Defaults to True.

        Returns:
            np.ndarray: (# params, 2) array of rank confidence intervals.
        """
        indices = self.model.get_indices(columns, self.exog_names)
        return (
            self._simultaneous_rank_conf_int(alpha, indices)
            if simultaneous
            else self._marginal_rank_conf_int(alpha, indices)
        )

    def _simultaneous_rank_conf_int(
        self, alpha: float, indices: np.ndarray
    ) -> np.ndarray:
        """Compute rank confidence intervals for simultaneous coverage.

        See :meth:`BayesResults.rank_conf_int` for arguments.
        """
        rank_rvs = (-self._posterior_rvs).argsort().argsort() + 1
        conf_int = self._marginal_rank_conf_int(alpha, self.model.get_indices())
        # (# samples,) array where indices i is the number of parameters in their rank
        # confidence interval for sample i
        n_in_conf_int = (
            (np.expand_dims(conf_int[:, 0], 0) <= rank_rvs)
            & (rank_rvs <= np.expand_dims(conf_int[:, 1], 0))
        ).sum(axis=1)
        conf_int_border = np.array([conf_int[:, 0] - 1, conf_int[:, 1] + 1]).T

        # probability that parameter i takes on rank j
        get_pr_i_ranked_j = (
            lambda i, j: self.rank_df.iloc[j - 1, i]
            if 0 < j <= self.model.n_params
            else 0
        )
        get_pr_border = lambda i, border: [
            get_pr_i_ranked_j(i, border[0]),
            get_pr_i_ranked_j(i, border[1]),
        ]
        pr_border = np.array(
            [get_pr_border(i, border) for i, border in enumerate(conf_int_border)]
        )

        while (n_in_conf_int == self.model.n_params).mean() < 1 - alpha:
            while (pr_border == 0).all():
                conf_int_border = np.array(
                    [conf_int_border[:, 0] - 1, conf_int_border[:, 1] + 1]
                ).T
                pr_border = np.array(
                    [
                        get_pr_border(i, border)
                        for i, border in enumerate(conf_int_border)
                    ]
                )
            # index is the (parameter, 0 for lower 1 for upper) that maximizes the
            # border confidence interval probability
            index = np.unravel_index(pr_border.argmax(), pr_border.shape)
            rank_rvs_i = rank_rvs[:, index[0]]
            if index[1]:
                # expand the upper bound of the confidence interval
                n_in_conf_int += (conf_int[index] < rank_rvs_i) & (
                    rank_rvs_i <= conf_int_border[index]
                )
                conf_int[index] = conf_int_border[index]
                conf_int_border[index] += 1
            else:
                # expand the lower bound of the confidence interval
                n_in_conf_int += (conf_int_border[index] <= rank_rvs_i) & (
                    rank_rvs_i < conf_int[index]
                )
                conf_int[index] = conf_int_border[index]
                conf_int_border[index] -= 1

            pr_border[index] = get_pr_i_ranked_j(index[0], conf_int_border[index])

        return conf_int[indices]

    def _marginal_rank_conf_int(self, alpha: float, indices: np.ndarray) -> np.ndarray:
        """Compute rank confidence intervals for marginal coverage.

        See :meth:`BayesResults.rank_conf_int` for arguments.
        """

        def compute_rank_ci(index):
            ci_upper = ci_lower = rank = param_rankings[index] - 1
            probabilities = self.rank_df.iloc[:, index].values
            coverage = probabilities[ci_upper]
            while coverage < 1 - alpha and ci_upper < self.model.n_params - 1:
                # entend upper bound of the confidence interval until coverage is achieved
                ci_upper += 1
                coverage += probabilities[ci_upper]

            while coverage < 1 - alpha and ci_lower > 0:
                # if the upper bound is at the maximum and coverage still isn't achieved,
                # entend the lower bound
                ci_lower -= 1
                coverage += probabilities[ci_lower]

            best_ci_lower, best_ci_upper = ci_lower, ci_upper
            while ci_upper >= rank and ci_lower >= 0 and coverage > 1 - alpha:
                # shift the confidence interval upward while maintaining coverage
                coverage -= probabilities[ci_upper]
                ci_upper -= 1
                while coverage < 1 - alpha and ci_lower > 0:
                    ci_lower -= 1
                    coverage += probabilities[ci_lower]

                if (
                    ci_upper - ci_lower < best_ci_upper - best_ci_lower
                    and coverage > 1 - alpha
                ):
                    # select the shortest confidence interval
                    best_ci_upper, best_ci_lower = ci_upper, ci_lower

            return [best_ci_lower, best_ci_upper]

        param_rankings = (-self.params).argsort().argsort() + 1
        return np.array([compute_rank_ci(i) for i in indices]) + 1

    def rank_point_plot(
        self,
        yname: str = None,
        xname: Sequence[str] = None,
        title: str = None,
        columns: ColumnsType = None,
        ax=None,
        **kwargs: Any,
    ):
        """Create a point plot.

        Args:
            yname (str, optional): Name of the endogenous variable. Defaults to None.
            xname (Sequence[str], optional): (# params,) sequence of parameter names.
                Defaults to None.
            title (str, optional): Plot title. Defaults to None.
            columns (ColumnsType, optional): Selected columns. Defaults to None.
            ax (AxesSubplot, optional): Axis to write on.
            **kwargs (Any): Passed to :meth:`ResultsBase.conf_int`.

        Returns:
            AxesSubplot: Plot.
        """
        indices = self.model.get_indices(columns, self.exog_names)
        params = (-self.params).argsort().argsort()[indices] + 1
        conf_int = self.rank_conf_int(columns=columns, **kwargs)
        yticks = np.arange(len(indices), 0, -1)

        if ax is None:
            _, ax = plt.subplots()
        ax.errorbar(
            x=params,  # type: ignore, pylint: disable=no-member
            y=yticks,
            xerr=[params - conf_int[:, 0], conf_int[:, 1] - params],  # type: ignore, pylint: disable=no-member
            fmt="o",
        )
        ax.set_title(title or self.title)
        ax.set_xlabel(yname or self.model.endog_names)
        ax.set_yticks(yticks)
        ax.set_yticklabels(self.exog_names[indices] if xname is None else xname)

        return ax

    def expected_wasserstein_distance(
        self, mean: Numeric1DArray = None, cov: np.ndarray = None, **kwargs: Any
    ) -> float:
        """Compute the Wasserstein distance metric.

        This method estimates the Wasserstein distance between the observed
        distribution (a joint normal characterized by ``mean`` and ``cov``) and the
        distribution you would expect to observe according to this model.

        Args:
            mean (Numeric1DArray, optional): (# params,) array of sample conventionally
                estimated means. If None, use the model's estimated means. Defaults to
                None.
            cov (np.ndarray, optional): (# params, # params) covaraince matrix for
                conventionally estimated means. If None, use the model's estimated
                covariance matrix. Defaults to None.
            **kwargs (Any): Keyword arguments for ``scipy.stats.wasserstein_distance``.

        Returns:
            float: Expected Wasserstein distance.
        """
        if mean is None and cov is None:
            mean = self.params
            reconstructed_rvs = self._reconstructed_rvs
        else:
            if cov is None:
                cov = self.model.cov
            reconstructed_rvs = np.apply_along_axis(
                lambda mean: multivariate_normal.rvs(mean, cov), 1, self._posterior_rvs
            )

        distances = np.apply_along_axis(
            lambda rv: wasserstein_distance(rv, mean, **kwargs), 1, reconstructed_rvs
        )
        return (self._sample_weight * distances).sum()

    def likelihood(self, mean: Numeric1DArray = None, cov: np.ndarray = None) -> float:
        """
        Args:
            mean (Numeric1DArray, optional): (# params,) array of sample conventionally
                estimated means. If None, use the model's estimated means. Defaults to
                None.
            cov (np.ndarray, optional): (# params, # params) covaraince matrix for
                conventionally estimated means. If None, use the model's estimated
                covariance matrix. Defaults to None.

        Returns:
            float: Likelihood.
        """
        if mean is None:
            mean = self.model.mean
        if cov is None:
            cov = self.model.cov

        return (
            self._sample_weight
            * multivariate_normal.pdf(self._posterior_rvs, mean, cov)
        ).sum()

    def line_plot(
        self,
        column: ColumnType = None,
        alpha: float = 0.05,
        title: str = None,
        yname: str = None,
        ax=None,
    ):
        """Create a line plot of the prior, conventional, and posterior estimates.

        Args:
            column (ColumnType, optional): Selected parameter. Defaults to None.
            alpha (float, optional): Sets the plot width. 0 is as wide as possible, 1 is
                as narrow as possible. Defaults to .05.
            title (str, optional): Plot title. Defaults to None.
            yname (str, optional): Name of the dependent variable. Defaults to None.
            ax (AxesSubplot, optional): Axis to write on.

        Returns:
            AxesSubplot: Plot.
        """
        index = self.model.get_index(column)
        prior = self.model.get_marginal_prior(index)
        posterior = self.marginal_distributions[index]
        conventional = norm(
            self.model.mean[index], np.sqrt(self.model.cov[index, index])
        )
        xlim = np.array(
            [
                dist.ppf([alpha / 2, 1 - alpha / 2])
                for dist in (prior, conventional, posterior)
            ]
        ).T
        x = np.linspace(xlim[0].min(), xlim[1].max())
        palette = sns.color_palette()
        if ax is None:
            _, ax = plt.subplots()
        sns.lineplot(x=x, y=prior.pdf(x), label="prior", ax=ax)
        ax.axvline(prior.mean(), linestyle="--", color=palette[0])
        sns.lineplot(x=x, y=conventional.pdf(x), label="conventional")
        ax.axvline(conventional.mean(), linestyle="--", color=palette[1])
        sns.lineplot(x=x, y=posterior.pdf(x), label="posterior")
        ax.axvline(posterior.mean(), linestyle="--", color=palette[2])
        ax.set_title(title or self.model.exog_names[index])
        ax.set_xlabel(yname or self.model.endog_names)
        return ax

    def rank_matrix_plot(self, title: str = None, **kwargs: Any):
        """Plot a heatmap of the rank matrix.

        Args:
            title (str, optional): Plot title. Defaults to None.
            **kwargs (Any): Passed to ``sns.heatmap``.

        Returns:
            AxesSubplot: Heatmap.
        """
        ax = sns.heatmap(self.rank_df, center=1 / self.model.n_params, **kwargs)
        ax.set_title(title or f"{self.title} rank matrix")
        return ax

    def reconstruction_point_plot(
        self,
        yname: str = None,
        xname: Sequence[str] = None,
        title: str = None,
        alpha: float = 0.05,
        ax=None,
    ):
        """Create  point plot of the reconstructed sample means.

        Plots the distribution of sample means you would expect to see if this model
        were correct.

        Args:
            yname (str, optional): Name of the endogenous variable. Defaults to None.
            xname (Sequence[str], optional): Names of x-ticks. Defaults to None.
            title (str, optional): Plot title. Defaults to None.
            alpha: (float, optional): Plot the 1-alpha CI. Defaults to 0.05.
            ax: (AxesSubplot, optional): Axis to write on.

        Returns:
            plt.axes._subplots.AxesSubplot: Plot.
        """
        reconstructed_means = -np.sort(-self._reconstructed_rvs)
        params = np.average(reconstructed_means, axis=0, weights=self._sample_weight)

        conf_int = np.apply_along_axis(
            weighted_quantile,
            0,
            reconstructed_means,
            quantiles=[alpha / 2, 1 - alpha / 2],
            sample_weight=self._sample_weight,
        ).T

        xname = xname or np.arange(self.model.n_params)
        yticks = np.arange(len(xname), 0, -1)
        if ax is None:
            _, ax = plt.subplots()
        ax.errorbar(
            x=params,
            y=yticks,
            xerr=[params - conf_int[:, 0], conf_int[:, 1] - params],
            fmt="o",
        )
        ax.set_title(title or f"{self.title} reconstruction plot")
        ax.set_xlabel(yname or self.model.endog_names)
        ax.set_ylabel("rank")
        ax.set_yticks(yticks)
        ax.set_yticklabels(xname)

        ax.errorbar(x=-np.sort(-self.model.mean), y=yticks, fmt="x")

        return ax

    def _make_summary_header(self, alpha: float) -> list[str]:
        return ["coef", "pvalue (1-sided)", f"[{alpha/2}", f"{1-alpha/2}]"]


class BayesBase(ModelBase):
    """Mixin for Bayesian models.

    Subclasses :class:`multiple_inference.base.ModelBase`.
    """

    _results_cls = BayesResults

    def get_marginal_prior(self, column: ColumnType) -> rv_continuous:
        """Get the marginal prior distribution of ``column``.

        Args:
            column (ColumnType): Name or index of the parameter of interest.

        Returns:
            rv_continuous: Prior distribution
        """
        return self._get_marginal_prior(self.get_index(column))

    def _get_marginal_prior(self, index: int) -> rv_continuous:
        """Private version of :meth:`self.get_marginal_prior`."""
        raise NotImplementedError()

    def get_marginal_distribution(self, column: ColumnType) -> rv_continuous:
        """Get the marginal posterior distribution of ``column``.

        Args:
            column (ColumnType): Name or index of the parameter of interest.

        Returns:
            rv_continuous: Posterior distribution.
        """
        return self._get_marginal_distribution(self.get_index(column))

    def _get_marginal_distribution(self, index: int) -> rv_continuous:
        """Private version of :meth:`self.get_marginal_distribution`."""
        raise NotImplementedError()

    def get_joint_prior(self, columns: ColumnsType = None):
        """Get the joint prior distribution.

        Args:
            columns (ColumnsType, optional): Selected columns. Defaults to None.

        Returns:
            rv_like: Joint distribution.
        """
        return self._get_joint_prior(self.get_indices(columns))

    def _get_joint_prior(self, indices: np.ndarray):
        """Private version of :meth:`self.get_joint_prior`."""
        return joint_distribution([self.get_marginal_prior(i) for i in indices])

    def get_joint_distribution(self, columns: ColumnsType = None):
        """Get the joint posterior distribution.

        Args:
            columns (ColumnsType, optional): Selected columns. Defaults to None.

        Returns:
            rv_like: Joint distribution.
        """
        return self._get_joint_distribution(self.get_indices(columns))

    def _get_joint_distribution(self, indices: np.ndarray):
        """Private version of :meth:`self.get_joint_distribution`."""
        raise NotImplementedError()
