import numpy as np
import pytest

from ncafs.core import add_pseudocount


class TestFunctions:
    @pytest.mark.parametrize("length, frac_zeros", [(10, 0.1), (10, 0.5), (10, 1), (100, 0), (100, 0.1), (100, 0.8)])
    def test_pseudocount(self, length, frac_zeros):
        A = np.random.rand(length, 1) + 0.5
        idx = np.arange(length)
        to_zero = np.random.choice(idx, size=round(length * frac_zeros), replace=False)
        A[to_zero] = 0
        A_pseudo = add_pseudocount(A)

        assert np.sum(A > 0) == round(length * (1 - frac_zeros))
        assert (A_pseudo > 0).all()
        assert A.shape == A_pseudo.shape
        assert np.alltrue(A[A > 0] == A_pseudo[A > 0])
