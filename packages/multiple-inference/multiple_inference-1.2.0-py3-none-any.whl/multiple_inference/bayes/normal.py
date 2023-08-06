"""Empirical Bayes with a normal prior.

References:

    .. code-block::

        @inproceedings{stein1956inadmissibility,
            title={Inadmissibility of the usual estimator for the mean of a multivariate normal distribution},
            author={Stein, Charles and others},
            booktitle={Proceedings of the Third Berkeley symposium on mathematical statistics and probability},
            volume={1},
            number={1},
            pages={197--206},
            year={1956}
        }

        @incollection{james1992estimation,
            title={Estimation with quadratic loss},
            author={James, William and Stein, Charles},
            booktitle={Breakthroughs in statistics},
            pages={443--460},
            year={1992},
            publisher={Springer}
        }

        @article{bock1975minimax,
            title={Minimax estimators of the mean of a multivariate normal distribution},
            author={Bock, Mary Ellen},
            journal={The Annals of Statistics},
            pages={209--218},
            year={1975},
            publisher={JSTOR}
        }

        @inproceedings{dimmery2019shrinkage,
            title={Shrinkage estimators in online experiments},
            author={Dimmery, Drew and Bakshy, Eytan and Sekhon, Jasjeet},
            booktitle={Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining},
            pages={2914--2922},
            year={2019}
        }

        @article{armstrong2020robust,
            title={Robust empirical bayes confidence intervals},
            author={Armstrong, Timothy B and Koles{\'a}r, Michal and Plagborg-M{\o}ller, Mikkel},
            journal={arXiv preprint arXiv:2004.03448},
            year={2020}
        }

Notes:

    The James-Stein method of fitting the normal prior relies on my own fully Bayesian
    derivation that extends Dimmery et al. (2019)'s derivation by 1) accounting for correlated
    errors and 2) allowing the prior mean vector to depend on a feature matrix ``X``.
"""
from __future__ import annotations

import math
import warnings
from typing import Any, Callable, Union

import numpy as np
from scipy.optimize import minimize_scalar, root_scalar
from scipy.stats import multivariate_normal, ncx2, norm, rv_continuous

from multiple_inference.base import ColumnsType
from multiple_inference.bayes.base import BayesBase, BayesResults


def compute_robust_critical_value(
    m2: float, kurtosis: float = np.inf, alpha: float = 0.05
) -> tuple[float, np.ndarray, np.ndarray]:
    """Compute the critical value for robust confidence intervals.

    Args:
        m2 (float): Equality constraint on :math:`E[b^2]`.
        kurtosis (float, optional): Estimated kurtosis of the prior distribution.
            Defaults to np.inf.
        alpha (float, optional): Significance level. Defaults to .05.

    Returns:
        tuple[float, np.ndarray, np.ndarray]: Critical value, array of :math:`x` values
        for the least favorable mass function, array of probabilities for the least
        favorable mass function.

    Notes:

        See Armstrong et al., 2020 for mathematical details. This function is equivalent
        to the ``cva`` function in the
        `ebci R package <https://cran.r-project.org/web/packages/ebci/index.html>`_ and
        uses the same variable names and tolerance thresholds.
    """

    def rho0(chi):
        t0 = rt0(chi)[0]
        return r(m2, chi) if m2 >= t0 else r(t0, chi) + (m2 - t0) * r1(t0, chi)

    def rt0(chi):
        # returns t0, inflection point
        # the inflection point is denoted t1 in the paper
        if (chi_sq := chi**2) < 3:
            return 0, 0

        if abs(r2(inflection := chi_sq - 1.5, chi=chi)) > tol:
            inflection = root_scalar(
                lambda x: r2(x, chi=chi), bracket=(chi_sq - 3, chi_sq), method="brentq"
            ).root

        func = lambda t: r(t, chi) - t * r1(t, chi) - r(0, chi)
        lower, upper = inflection, 2 * chi_sq
        t0 = (
            root_scalar(lambda x: func(x), bracket=(lower, upper), method="brentq").root
            if func(lower) < 0
            else lower
        )
        return t0, inflection

    def r(t, chi):
        # called r0 in the paper
        sqrt_t = np.sqrt(t)
        return (
            (norm.cdf(-sqrt_t - chi) + norm.cdf(sqrt_t - chi))
            if sqrt_t - chi < 5
            else 1
        )

    def r1(t, chi):
        # first derivative of r
        sqrt_t = np.sqrt(t)
        if t < 1e-8:
            # apply L'Hopital's rule
            return chi * norm.pdf(chi)
        return (norm.pdf(sqrt_t - chi) - norm.pdf(sqrt_t + chi)) / (2 * sqrt_t)

    def r2(t, chi):
        # second derivative of r
        sqrt_t = np.sqrt(t)
        if t < 2e-6:
            # apply L'Hopital's rule
            return chi * (chi**2 - 3) * norm.pdf(chi) / 6
        coef0 = chi * sqrt_t
        coef1 = t + 1
        return (
            (coef0 + coef1) * norm.pdf(sqrt_t + chi)
            + (coef0 - coef1) * norm.pdf(sqrt_t - chi)
        ) / (4 * t**1.5)

    def r3(t, chi):
        # third derivative of r
        sqrt_t = np.sqrt(t)
        if t < 2e-4:
            # apply L'Hopital's rule
            return (chi**5 - 10 * chi**3 + 15 * chi) * norm.pdf(chi) / 60
        coef0 = t**2 + (2 + chi**2) * t + 3
        coef1 = 2 * chi * t**1.5 + 3 * chi * sqrt_t
        return (
            (coef0 - coef1) * norm.pdf(chi - sqrt_t)
            - (coef0 + coef1) * norm.pdf(chi + sqrt_t)
        ) / (8 * t**2.5)

    def rho(chi):
        # return (optimum loss, x values for pmf, probabilities for pmf)
        if kurtosis == 1:
            return r(m2, chi), np.array([0, m2]), np.array([0, 1])

        r0, t0 = rho0(chi), rt0(chi)[0]
        if m2 >= t0:
            return r0, np.array([0, m2]), np.array([0, 1])

        if kurtosis == np.inf or m2 * kurtosis >= t0:
            return r0, np.array([0, t0]), np.array([1 - m2 / t0, m2 / t0])

        tbar = lam(0, chi)[1]
        lammax = lambda x0: delta(0, x0, chi) if x0 >= tbar else max(lam(x0, chi)[0], 0)
        loss = (
            lambda x0: r(x0, chi)
            + (m2 - x0) * r1(x0, chi)
            + (kurtosis * m2**2 - 2 * x0 * m2 + x0**2) * lammax(x0)
        )
        result_above = minimize_scalar(loss, bounds=(tbar, t0), method="bounded")
        if tbar > 0:
            result_below = minimize_scalar(loss, bounds=(0, tbar), method="bounded")
            minimum_below, fun_below = result_below.x, result_below.fun
        else:
            minimum_below, fun_below = 0, loss(0)
        minimum, fun = (
            (result_above.x, result_above.fun)
            if result_above.fun < fun_below
            else (minimum_below, fun_below)
        )

        values = np.sort([minimum, lam(minimum, chi)[1]])
        probability = (m2 - values[1]) / (values[0] - values[1])
        return fun, values, np.array([probability, 1 - probability])

    def lam(x0, chi):
        # returns delta(x*, x0, chi), x*
        # where x* = argmax_x(delta(x, x0, chi))
        # check 0, inflection point, t0, and x0
        x = np.sort(rt0(chi))
        x = np.array([0, x[0]]) if x0 >= x[0] else np.unique([0, x0, *x])
        derivatives = delta1(x, x0, chi)
        values = delta(x, x0, chi)
        optimum = values[0], 0
        if (derivatives <= 0).all() and values.argmax() == 0:
            return optimum

        if (np.diff(derivatives >= 0) >= 0).all() and derivatives[-1] <= 0:
            index = max((derivatives >= 0).argmin(), 1)
            bounds = x[index - 1], x[index]
        elif abs(derivatives).min() < 1e-6:
            argmax = values.argmax()
            bounds = x[max(argmax - 1, 0)], x[min(argmax + 1, len(values) - 1)]
        else:
            raise RuntimeError(
                f"There are multiple optima in the function delta(x, x0={x0}, chi={chi})."
            )

        result = minimize_scalar(
            lambda x: -delta(x, x0, chi), bounds=bounds, method="bounded"
        )
        return (-result.fun, result.x) if -result.fun > optimum[0] else optimum

    def delta(x, x0, chi):
        def func(x):
            return (
                0.5 * r2(x0, chi)  # apply L'Hopital's rule
                if abs(x - x0) < 1e-4
                else (r(x, chi) - r(x0, chi) - (x - x0) * r1(x0, chi)) / (x - x0) ** 2
            )

        return func(x) if np.isscalar(x) else np.array([func(x_i) for x_i in x])

    def delta1(x, x0, chi):
        # first derivative of delta
        def func(x):
            if abs(x - x0) < 1e-3:
                # apply L'Hoptial's rule
                return r3(x0, chi)
            return (
                r1(x, chi) + r1(x0, chi) - 2 * (r(x, chi) - r(x0, chi)) / (x - x0)
            ) / (x - x0) ** 2

        return func(x) if np.isscalar(x) else np.array([func(x_i) for x_i in x])

    tol = 1e-12
    critical_value_b = (
        np.sqrt(ncx2.ppf(1 - alpha, nc=m2, df=1))
        if m2 < 100
        else norm.ppf(1 - alpha, np.sqrt(m2))
    )
    if m2 == 0 or kurtosis == 1:
        return critical_value_b, np.array([0, m2]), np.array([0, 1])

    if m2 > 1 / tol and kurtosis != np.inf:
        kurtosis = np.inf

    # get bounds for when kappa == 1 and kappa == infinity
    lower, upper = critical_value_b - 0.01, np.sqrt((m2 + 1) / alpha)
    if abs(rho0(upper) - alpha) > 9e-6:
        upper = root_scalar(
            lambda chi: rho0(chi) - alpha, bracket=(lower, upper), method="brentq"
        ).root

    if rho(upper)[0] - alpha < -1e-5:
        critical_value = root_scalar(
            lambda chi: rho(chi)[0] - alpha, bracket=(lower, upper), method="brentq"
        ).root
    else:
        critical_value = upper
    return critical_value, *rho(critical_value)[1:]


class NormalResults(BayesResults):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # estimate constraints and kurtosis for computing robust confidence intervals
        # constraints are denoted "m2" in Armstrong et al., 2020
        self._robust_conf_int_constraints = (
            self.model.cov.diagonal() / self.model.prior_cov.diagonal()
        )
        cov_inv = np.linalg.inv(self.model.cov)
        weights = (
            np.linalg.inv(self.model.X.T @ cov_inv @ self.model.X)
            @ self.model.X.T
            @ cov_inv
        )
        error = self.model.mean - self.model.prior_mean
        cov_diag = self.model.cov.diagonal()
        prior_cov_diag = self.model.prior_cov.diagonal()
        kurtosis0 = (
            weights * (error**4 - 6 * cov_diag * error**2 + 3 * cov_diag**2)
        ).sum() / (weights * prior_cov_diag**2).sum()
        kurtosis1 = (
            1
            + 32
            * (weights**2 * cov_diag**4).sum()
            / (weights * (prior_cov_diag**2 + cov_diag**2)).sum()
        )
        self._kurtosis = max(kurtosis0, kurtosis1)

    def conf_int(
        self,
        alpha: float = 0.05,
        columns: ColumnsType = None,
        robust: bool = False,
        fast: bool = False,
        **kwargs: Any,
    ) -> np.ndarray:
        """Compute the 1-alpha confidence interval.

        Args:
            alpha (float, optional): Significance level. Defaults to .05.
            columns (ColumnsType, optional): Selected columns. Defaults to None.
            robust (bool, optional): Use robust confidence intervals. These will have
                correct average coverage even if the normal prior assumption is
                violated. Defaults to False.
            fast (bool, optional): Use a "fast" computation method for the robust
                confidence intervals. This assumes the critical value is the same for
                all parameters. Defaults to False.

        Returns:
            np.ndarray: (# params, 2) array of confidence intervals.
        """
        if not robust:
            return super().conf_int(alpha, columns, **kwargs)

        indices = self.model.get_indices(columns)
        constraints = self._robust_conf_int_constraints[indices]
        if fast or np.isclose(constraints, constraints[0]).all():
            constraint = constraints.mean()
            critical_values = np.full(
                len(constraints),
                [compute_robust_critical_value(constraint, self._kurtosis, alpha)[0]],
            )
        else:
            critical_values = np.array(
                [
                    compute_robust_critical_value(x, self._kurtosis, alpha)[0]
                    for x in constraints
                ]
            )
        len_conf_int = critical_values * np.sqrt(
            self.model.posterior_cov.diagonal()[indices]
        )
        params = self.params[indices]
        return np.array([params - len_conf_int, params + len_conf_int]).T


class Normal(BayesBase):
    """Bayesian model with a normal prior.

    Args:
        fit_method (Union[str, Callable[[], None]], optional): Specifies how to fit the
            prior ("mle", "bock", or "james_stein"). You can also use a custom function
            that sets the ``prior_mean``, ``prior_cov``, ``posterior_mean`` and
            ``posterior_cov`` attributes. Defaults to "mle".
        prior_mean (Union[float, np.ndarray], optional): (# params,) prior mean vector.
            Defaults to None.
        prior_cov (Union[float, np.ndarray], optional): (# params, # params) prior
            covariance matrix. Defaults to None.

    Examples:

        .. testcode::

            import numpy as np
            from multiple_inference.bayes import Normal

            model = Normal(np.arange(10), np.identity(10))
            results = model.fit()
            print(results.summary())

        .. testoutput::
            :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

                       Bayesian estimates
            =======================================
                coef pvalue (1-sided) [0.025 0.975]
            ---------------------------------------
            x0 0.545            0.282 -1.305  2.395
            x1 1.424            0.066 -0.426  3.274
            x2 2.303            0.007  0.453  4.153
            x3 3.182            0.000  1.332  5.032
            x4 4.061            0.000  2.211  5.911
            x5 4.939            0.000  3.089  6.789
            x6 5.818            0.000  3.968  7.668
            x7 6.697            0.000  4.847  8.547
            x8 7.576            0.000  5.726  9.426
            x9 8.455            0.000  6.605 10.305
            ===============
            Dep. Variable y
            ---------------
    """

    _results_cls = NormalResults

    def __init__(
        self,
        *args: Any,
        fit_method: Union[str, Callable[[], None]] = "mle",
        prior_mean: Union[float, np.ndarray] = None,
        prior_cov: Union[float, np.ndarray] = None,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.prior_mean, self.prior_cov = prior_mean, prior_cov
        if np.isscalar(prior_mean):
            self.prior_mean = np.full(self.n_params, prior_mean)
        if np.isscalar(prior_cov):
            self.prior_cov = prior_cov * np.identity(self.n_params)

        self.posterior_mean, self.posterior_cov = None, None
        if callable(fit_method):
            fit_method()
            self._set_posterior_estimates()
        else:
            fit_methods = {
                "mle": self._fit_mle,
                "james_stein": self._fit_james_stein,
                "bock": self._fit_bock,
            }
            if fit_method not in fit_methods:
                raise ValueError(
                    f"`fit_method` must be one of {fit_methods.keys()}, got {fit_method}."
                )
            fit_methods[fit_method]()

    def _fit_mle(self, max_iter: int = 100, rtol: float = 0.99) -> None:
        """Fit the model using maximum likelihood estimation.

        Args:
            max_iter (int, optional): Maximum number of EM iterations. Defaults to 100.
            rtol (float, optional): Stopping criterion for EM. Defaults to .99.
        """

        def neg_log_likelihood(prior_std):
            # negative log likelihood as a function of the prior standard deviation
            marginal_cov = prior_std**2 * np.identity(self.n_params) + self.cov
            # note: the prior mean is also the marginal mean
            return -multivariate_normal.logpdf(self.mean, prior_mean, marginal_cov)

        # use EM to iteratively update the prior mean and covariance
        prior_cov = (
            np.zeros(self.cov.shape) if self.prior_cov is None else self.prior_cov
        )
        current_log_likelihood, prev_log_likelihood = None, -np.inf
        for _ in range(max_iter):
            # update prior mean
            if self.prior_mean is not None:
                prior_mean = self.prior_mean
            else:
                marginal_cov_inv = np.linalg.inv(self.cov + prior_cov)
                prior_mean = (
                    self.X
                    @ np.linalg.inv(self.X.T @ marginal_cov_inv @ self.X)
                    @ self.X.T
                    @ marginal_cov_inv
                    @ self.mean
                )

            # update prior cov
            if self.prior_cov is not None:
                prior_cov = self.prior_cov
                break  # prior_mean is computed analytically, so no need to iterate futher
            else:
                result = minimize_scalar(
                    neg_log_likelihood, bounds=(0, self.mean.std()), method="bounded"
                )
                prior_cov = result.x**2 * np.identity(self.n_params)
                current_log_likelihood = -result.fun

            if current_log_likelihood / prev_log_likelihood > rtol:
                break
            prev_log_likelihood = current_log_likelihood

        # set the posterior mean and covariance estimates
        # and adjust the prior and posterior covariances to account for uncertainty in the MLE estimate of the prior mean
        prior_uncertainty = post_uncertainty = 0
        if self.prior_mean is None:
            marginal_cov_inv = np.linalg.inv(prior_cov + self.cov)
            prior_uncertainty = (
                self.X @ np.linalg.inv(self.X.T @ marginal_cov_inv @ self.X) @ self.X.T
            )
            xi = self.cov @ marginal_cov_inv
            post_uncertainty = xi @ prior_uncertainty @ xi

        self.prior_mean, self.prior_cov = prior_mean, prior_cov
        self._set_posterior_estimates()  # note: set the posterior estimates *before* adjusting the prior covariance
        self.prior_cov += prior_uncertainty
        self.posterior_cov += post_uncertainty

    def _fit_bock(self, max_iter: int = 100, rtol: float = 0.99) -> None:
        """Fit the model using Bock (1975)'s multivariate Stein-type estimator.

        Args:
            max_iter (int, optional): Maximum number of iterations. Defaults to 100.
            rtol (float, optional): Stopping criteria. Defaults to .99.

        Raises:
            RuntimeError: The shrinkage factor must be positve.
        """
        cov_inv = np.linalg.inv(self.cov)
        prior_mean_df = self.X.shape[1] if self.prior_mean is None else 0
        effective_dimension = np.trace(self.cov) / np.linalg.eig(self.cov)[0].max()
        if effective_dimension - prior_mean_df - 2 < 0:
            raise RuntimeError(
                "Failed to fit the Bock (1975) estimator because the effective dimension"
                " of the covariance matrix is too small. Try another fit method like"
                " 'mle'."
            )

        xi = (
            np.identity(self.n_params)
            if self.prior_cov is None
            else self.cov @ np.linalg.inv(self.cov + self.prior_cov)
        )
        current_log_likelihood, prev_log_likelihood = None, -np.inf
        for _ in range(max_iter):
            if self.prior_mean is None:
                # update prior mean
                marginal_cov_inv = cov_inv @ xi
                prior_mean = (
                    self.X
                    @ np.linalg.inv(self.X.T @ marginal_cov_inv @ self.X)
                    @ self.X.T
                    @ marginal_cov_inv
                    @ self.mean
                )
            else:
                prior_mean = self.prior_mean

            if self.prior_cov is None:
                # update prior covariance
                error = self.mean - prior_mean
                param = min(
                    (effective_dimension - prior_mean_df - 2)
                    / (error.T @ cov_inv @ error),
                    1,
                )
                xi = param * np.identity(self.n_params)
            else:
                prior_cov = self.prior_cov
                # prior mean is computed analytically, so no need to iterate
                break

            # check for convergence
            marginal_cov = np.linalg.inv(xi) @ self.cov
            prior_cov = marginal_cov - self.cov
            current_log_likelihood = multivariate_normal.logpdf(
                self.mean, prior_mean, marginal_cov
            )
            if current_log_likelihood / prev_log_likelihood > rtol:
                break
            prev_log_likelihood = current_log_likelihood

        # set the posterior mean and covariance estimates
        # and adjust the prior and posterior covariances to account for uncertainty in the MLE estimate of the prior mean
        prior_uncertainty = post_uncertainty = 0
        if self.prior_mean is None:
            marginal_cov_inv = np.linalg.inv(prior_cov + self.cov)
            prior_uncertainty = (
                self.X @ np.linalg.inv(self.X.T @ marginal_cov_inv @ self.X) @ self.X.T
            )
            xi = self.cov @ marginal_cov_inv
            post_uncertainty = xi @ prior_uncertainty @ xi

        self.prior_mean, self.prior_cov = prior_mean, prior_cov
        self._set_posterior_estimates()  # note: set the posterior estimates *before* adjusting the prior covariance
        self.prior_cov += prior_uncertainty
        self.posterior_cov += post_uncertainty

    def _set_posterior_estimates(self):
        """Sets the posterior mean and covariance using plugin estimates from the prior
        mean and covariance if the posterior parameters haven't already been set.
        """
        xi = self.cov @ np.linalg.inv(self.prior_cov + self.cov)
        if self.posterior_mean is None:
            self.posterior_mean = self.prior_mean + (
                np.identity(self.n_params) - xi
            ) @ (self.mean - self.prior_mean)

        if self.posterior_cov is None:
            self.posterior_cov = (np.identity(self.n_params) - xi) @ self.cov

    def _fit_james_stein(self, max_iter: int = 100, tol: float = 1e-6) -> None:
        """Fit the model using James-Stein estimates.

        Args:
            max_iter (int, optional): Maximum number of iterations to find the
                positive-part prior covariance.. Defaults to 100.
            tol (float, optional): Stopping criteria for finding the positive-part prior
                covariance. Defaults to 1e-6.
        """
        if self.prior_mean is None:
            prior_mean = (
                self.X @ np.linalg.inv(self.X.T @ self.X) @ self.X.T @ self.mean
            )
            prior_mean_df = self.X.shape[1]
        else:
            prior_mean = self.prior_mean
            prior_mean_df = 0

        s_squared = ((self.mean - prior_mean) ** 2).sum()
        try:
            np.linalg.cholesky(
                s_squared
                / (self.n_params - prior_mean_df - 2)
                * np.identity(self.n_params)
                - self.cov
            )
        except np.linalg.LinAlgError:
            # find minimum s_squared such that the (unadjusted) prior covariance is positive semidefinite
            warnings.warn(
                "The James-Stein prior covariance estimate is not positive semidefinite."
                " Using the positive-part James-Stein covariance estimate instead."
                " This may result in too little shrinkage."
            )
            bounds = [np.sqrt(s_squared), np.inf]
            for _ in range(max_iter):
                s_squared = (
                    2 * bounds[0] if bounds[1] == np.inf else sum(bounds) / 2
                ) ** 2
                try:
                    np.linalg.cholesky(
                        s_squared
                        / (self.n_params - prior_mean_df - 2)
                        * np.identity(self.n_params)
                        - self.cov
                    )
                    bounds[1] = np.sqrt(s_squared)
                except:
                    bounds[0] = np.sqrt(s_squared)
                if bounds[1] - bounds[0] < tol:
                    break
            s_squared = bounds[1] ** 2

        # compute the prior covariance
        param = s_squared / (self.n_params - prior_mean_df - 4)
        self.prior_cov = (
            param * np.identity(self.n_params)
            - self.cov
            + param * self.X @ np.linalg.inv(self.X.T @ self.X) @ self.X.T
        )

        # compute the posterior mean
        xi = self.cov * (self.n_params - prior_mean_df - 2) / s_squared
        self.posterior_mean = prior_mean + (np.identity(self.n_params) - xi) @ (
            self.mean - prior_mean
        )

        # compute the posterior covariance
        plugin_posterior_cov = (np.identity(self.n_params) - xi) @ self.cov
        if self.prior_mean is None:
            prior_mean_uncertainty = (
                self.cov @ self.X @ np.linalg.inv(self.X.T @ self.X) @ self.X.T @ xi
            )
        else:
            prior_mean_uncertainty = 0
        prior_cov_uncertainty = (
            2
            / (self.n_params - self.X.shape[1] - 2)
            * xi
            @ (self.mean - prior_mean).reshape(-1, 1)
            @ (self.mean - prior_mean).reshape(1, -1)
            @ xi
        )
        self.posterior_cov = (
            plugin_posterior_cov + prior_mean_uncertainty + prior_cov_uncertainty
        )

        self.prior_mean = prior_mean

    def _get_marginal_prior(self, index: int) -> rv_continuous:
        return norm(self.prior_mean[index], np.sqrt(self.prior_cov[index, index]))

    def _get_marginal_distribution(self, index: int) -> rv_continuous:
        return norm(
            self.posterior_mean[index], np.sqrt(self.posterior_cov[index, index])
        )

    def _get_joint_prior(self, indices: np.ndarray):
        return multivariate_normal(
            self.prior_mean[indices],
            self.prior_cov[indices][:, indices],
            allow_singular=True,
        )

    def _get_joint_distribution(self, indices: np.ndarray):
        return multivariate_normal(
            self.posterior_mean[indices],
            self.posterior_cov[indices][:, indices],
            allow_singular=True,
        )
