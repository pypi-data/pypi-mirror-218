import pytest
from sklearn import datasets

from ncafs import NCAFSR, NCAFSC


eps = 1e-3


class TestRegression:
    @pytest.mark.parametrize("n_features, n_informative", [(20, 5), (20, 10), (20, 15), (40, 10), (40, 20)])
    def test_toy_dataset(self, n_features, n_informative):
        X, y, coef = datasets.make_regression(
            n_samples=1000,
            n_features=n_features,
            n_informative=n_informative,
            bias=0,
            noise=1e-3,
            coef=True,
            shuffle=False,
            random_state=0
        )

        fs_reg = NCAFSR()
        fs_reg.fit(X, y)
        w = fs_reg.weights_
        n_select = len(w[w > eps])
        assert 0.8 * n_informative - 0.1 * n_features <= n_select <= 1.2 * n_informative + 0.1 * n_features

    @pytest.mark.parametrize("n_features", [10, 20, 40, 60, 100])
    def test_friedman1(self, n_features):
        X, y = datasets.make_friedman1(n_samples=1000, n_features=n_features, noise=1e-1)
        fs_reg = NCAFSR()
        fs_reg.fit(X, y)
        w = fs_reg.weights_
        assert len(w[w > 1e-3]) == 5

    @pytest.mark.parametrize("n_features", [10, 20, 40, 60, 100])
    def test_sparse_uncorrelated(self, n_features):
        X, y = datasets.make_sparse_uncorrelated(n_samples=1000, n_features=n_features)
        fs_reg = NCAFSR()
        fs_reg.fit(X, y)
        w = fs_reg.weights_
        assert len(w[w > eps]) == 4


class TestClassification:
    @pytest.mark.parametrize("n_features, n_informative", [(20, 5), (20, 10), (20, 15), (40, 10), (40, 20),
                                                           (100, 10), (100, 40)])
    def test_toy_dataset(self, n_features, n_informative, n_redundant=0, n_repeated=0):
        X, y = datasets.make_classification(
            n_samples=1000,
            n_classes=5,
            n_features=n_features,
            n_informative=n_informative,
            n_redundant=n_redundant,
            n_repeated=n_repeated,
            flip_y=0.1,
            class_sep=0.5,
            shuffle=False,
            random_state=0
        )
        fs_class = NCAFSC()
        fs_class.fit(X, y)
        w = fs_class.weights_
        n_select = len(w[w > eps])
        assert 0.8*n_informative <= n_select <= 1.2*n_informative
