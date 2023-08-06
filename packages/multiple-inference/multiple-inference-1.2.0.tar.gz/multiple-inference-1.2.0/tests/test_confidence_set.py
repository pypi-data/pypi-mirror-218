import numpy as np
import pytest
from scipy.stats import norm

# test for large numbers of params
# test with groups

from multiple_inference.confidence_set import (
    ConfidenceSet,
    AverageComparison,
    BaselineComparison,
    PairwiseComparison,
    MarginalRanking,
    SimultaneousRanking,
)

N_PARAMS = 3
MEAN = np.arange(N_PARAMS) - (N_PARAMS - 1) / 2
COV = np.identity(N_PARAMS)


@pytest.mark.parametrize(
    "cls",
    (
        ConfidenceSet,
        AverageComparison,
        BaselineComparison,
        PairwiseComparison,
        MarginalRanking,
        SimultaneousRanking,
    ),
)
def test_common_methods(cls):
    # test that the common methods (conf_int, summary, point_plot) can run on all
    # classes without error
    kwargs = {"baseline": 0} if cls is BaselineComparison else {}
    results = cls(MEAN, COV, **kwargs).fit()
    results.conf_int()
    results.summary()
    if cls not in (MarginalRanking, SimultaneousRanking):
        results.test_hypotheses()
    results.point_plot()


class TestConfidenceSet:
    results = ConfidenceSet(MEAN, COV).fit()

    def test_conf_int_shape(self):
        assert self.results.conf_int().shape == (N_PARAMS, 2)

    def test_1_param(self):
        np.testing.assert_equal(
            ConfidenceSet(0, 1).fit().conf_int(), [norm.ppf([0.025, 0.975])]
        )

    def test_conf_int(self):
        # test the the marginal CI is in the simultaneous CI
        alpha = 0.05
        simultaneous_ci = self.results.conf_int(alpha)
        marginal_ci = np.array(
            [
                norm.ppf([alpha / 2, 1 - alpha / 2], mean, np.sqrt(var))
                for mean, var in zip(MEAN, COV.diagonal())
            ]
        )
        np.testing.assert_array_less(simultaneous_ci[:, 0], marginal_ci[:, 0])
        np.testing.assert_array_less(marginal_ci[:, 1], simultaneous_ci[:, 1])

    @pytest.mark.parametrize("two_tailed", (True, False))
    def test_test_hypotheses(self, two_tailed):
        results = ConfidenceSet([-3, -2, 0, 2, 3], np.identity(5)).fit()
        values = results.test_hypotheses(two_tailed=two_tailed)
        if two_tailed:
            np.testing.assert_array_equal(
                values,
                [
                    [False, True],  # significantly less than 0
                    [False, False],
                    [False, False],
                    [False, False],
                    [True, False],  # significantly greater than 0
                ],
            )
        else:
            np.testing.assert_array_equal(values, [False, False, False, False, True])


class TestAverageComparison:
    def test___init__(self):
        model = AverageComparison(MEAN, COV)
        np.testing.assert_almost_equal(model.mean, [-1, 0, 1])
        np.testing.assert_almost_equal(
            model.cov,
            [[2 / 3, -1 / 3, -1 / 3], [-1 / 3, 2 / 3, -1 / 3], [-1 / 3, -1 / 3, 2 / 3]],
        )


class TestBaselineComparison:
    def test___init__(self):
        model = BaselineComparison(MEAN, COV, baseline=0)
        np.testing.assert_almost_equal(model.mean, [1, 2])
        np.testing.assert_almost_equal(model.cov, [[2, 1], [1, 2]])


class TestPairwiseComparison:
    def test___init__(self):
        results = PairwiseComparison(MEAN, COV).fit()
        np.testing.assert_array_equal(
            results.exog_names, ["x1 - x0", "x2 - x0", "x2 - x1"]
        )
        np.testing.assert_almost_equal(results.params, [1, 2, 1])  # [1-0, 2-0, 2-1]
        np.testing.assert_almost_equal(results._std_diagonal, np.sqrt([2, 2, 2]))

    def test_conf_int_shape(self):
        results = PairwiseComparison(np.arange(4), np.identity(4)).fit()
        assert results.conf_int().shape[0] == 4 * (4 - 1) / 2

    @pytest.mark.parametrize("columns", (None, ["x2", "x1"]))
    @pytest.mark.parametrize("criterion", ("fdr", "fwer"))
    def test_test_hypotheses(self, columns, criterion):
        results = PairwiseComparison([0, 4, 1, 2], np.identity(4) / 3).fit()
        if columns is None:
            if criterion == "fwer":
                expected_values = [
                    [False, True, False, False],  # x1 > 0
                    [False, False, False, False],
                    [False, True, False, False],  # x1 > x2
                    [False, False, False, False],
                ]
            else:
                expected_values = [
                    [False, True, False, True],
                    [True, False, True, True],
                    [False, True, False, False],
                    [True, True, False, False],
                ]
        else:
            if criterion == "fwer":
                expected_values = [[False, True], [False, False]]
            else:
                expected_values = [[False, True], [True, False]]

        np.testing.assert_array_equal(
            results.test_hypotheses(criterion=criterion, columns=columns).values,
            expected_values,
        )

    def test_large_n_params(self, n_params=500):
        results = PairwiseComparison(np.arange(n_params), np.identity(n_params)).fit(
            n_samples=1000
        )
        results.summary()
        results.test_hypotheses()

    @pytest.mark.parametrize("triangular", (True, False))
    def test_hypothesis_heatmap(self, triangular):
        PairwiseComparison(MEAN, COV).fit().hypothesis_heatmap(triangular=triangular)


@pytest.fixture(scope="module")
def pairwise_groups(n_params=5):
    # make groups of (x0, x2, x4) and (x1, x3)
    groups = np.full(n_params, 0)
    groups[[i for i in range(n_params) if i % 2 == 1]] = 1
    return PairwiseComparison(np.arange(n_params), np.identity(n_params)).fit(
        groups=groups
    )


class TestPairwiseGroups:
    def test_exog_names(self, pairwise_groups):
        np.testing.assert_equal(
            pairwise_groups.exog_names, ["x2 - x0", "x4 - x0", "x4 - x2", "x3 - x1"]
        )

    def test_test_hypotheses(self, pairwise_groups):
        results = pairwise_groups.test_hypotheses()
        assert results[0].shape == (3, 3)  # group of x0, x2, x4
        assert results[1].shape == (2, 2)  # group of x1, x3

    def test_hypothesis_heatmap(self, pairwise_groups):
        pairwise_groups.hypothesis_heatmap()


class TestMarginalRanking:
    @pytest.mark.parametrize("columns", (None, ["x2", "x1"]))
    def test_conf_int(self, columns):
        # x0 is ranked 1 or 2
        # s1 is ranked 0, 1, or 2
        # x2 is ranked 0 or 1
        results = MarginalRanking(MEAN, COV / 3).fit()
        if columns is None:
            expected_values = [[2, 3], [1, 3], [1, 2]]
        else:
            expected_values = [[1, 2], [1, 3]]
        np.testing.assert_array_equal(
            results.conf_int(columns=columns), expected_values
        )


class TestSimultaneousRanking:
    @pytest.mark.parametrize("columns", (None, ["x2", "x1"]))
    def test_conf_int(self, columns):
        # x0 is ranked 1 or 2
        # s1 is ranked 0, 1, or 2
        # x2 is ranked 0 or 1
        results = SimultaneousRanking(MEAN, COV / 3).fit()
        if columns is None:
            expected_values = [[2, 3], [1, 3], [1, 2]]
        else:
            expected_values = [[1, 2], [1, 3]]
        np.testing.assert_array_equal(
            results.conf_int(columns=columns), expected_values
        )

    @pytest.mark.parametrize("n_best_params", (1, 2))
    @pytest.mark.parametrize("superset", (True, False))
    def test_compute_best_params(self, n_best_params, superset):
        # these parameters are from the stylized example in Mogstad's Inference for
        # Rankings paper
        x = np.array([3.3, 4.1, 4.2, 4.3, 6.2])
        cov = np.array(
            [
                [0.01, 0, 0, 0, 0],
                [0, 0.25, 0, 0, 0],
                [0, 0, 0.05, 0, 0],
                [0, 0, 0, 0.05, 0],
                [0, 0, 0, 0, 0.05],
            ]
        )
        results = SimultaneousRanking(x, cov).fit()
        if n_best_params == 1:
            # 95% chance x4 is the best parameter
            if superset:
                expected_values = [False, False, False, False, True]
            else:
                expected_values = [False, False, False, False, True]
        else:
            if superset:
                # 95% chance the two best parameters are x1-x4
                expected_values = [False, True, True, True, True]
            else:
                # 95% chance that x4 is in the two best parameters
                expected_values = [False, False, False, False, True]
        np.testing.assert_array_equal(
            results.compute_best_params(n_best_params, superset=superset).values,
            expected_values,
        )

    def test_large_n_params(self, n_params=500):
        results = SimultaneousRanking(np.arange(n_params), np.identity(n_params)).fit(
            n_samples=1000
        )
        results.summary()
        results.compute_best_params()
