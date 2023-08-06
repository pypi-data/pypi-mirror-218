"""Test PPR functions"""

import unittest
import numpy as np
from numpy.testing import assert_allclose
import pyppr

class TestPPRFunctions(unittest.TestCase):

    def test_ppr_net_fv(self):
        assert_allclose(pyppr.ppr_net_fv(0.07, 20, 10000, 0.0075, 0), 31424.830223144)
        assert_allclose(pyppr.ppr_net_fv(0.07, 20, 2000, 0.0075, 0.2), 7541.9592535546)
        assert_allclose(pyppr.ppr_net_fv(0.07, 20, 2000, 0.0075, np.array([0, 0.2])), [6284.9660446288, 7541.9592535546])
        assert_allclose(pyppr.ppr_net_fv(0.07, 20, np.array([10000, 2000]), 0.0075, np.array([0, 0.2])), [31424.830223144, 7541.9592535546])

    def test_matching_ppr_cost_rate(self):
        assert_allclose(pyppr.matching_ppr_cost_rate(0.07, 30, 0.28, 0.1, 0), 0.003749355)
        assert_allclose(pyppr.matching_ppr_cost_rate(0.07, 30, 0.28, 0.1, 0.2), 0.009870102)
        assert_allclose(pyppr.matching_ppr_cost_rate(0.07, 30, 0.28, 0.1, np.array([0, 0.2])), [0.003749355, 0.009870102])

    def test_matching_underlying_assets_cagr(self):
        assert_allclose(pyppr.matching_underlying_assets_cagr(20, 0.28, 0.05, 0.0075, 0), 0.0941281436701107)
        assert_allclose(pyppr.matching_underlying_assets_cagr(20, 0.28, 0.1, 0.0075, 0.2), 0.0149095359038968)
        assert_allclose(pyppr.matching_underlying_assets_cagr(20, 0.28, np.array([0.05, 0.1]), 0.0075, np.array([0, 0.2])), [0.0941281436701107, 0.0149095359038968])

    def matching_ppr_extra_value(self):
        assert_allclose(pyppr.matching_ppr_extra_value(0.07, 20, 0.28, 0.0075, 0), 0.0248877718180402)
        assert_allclose(pyppr.matching_ppr_extra_value(0.07, 20, 0.28, 0.0075, 0.2), 0.229865326181649)
        assert_allclose(pyppr.matching_ppr_cost_rate(0.07, 20, 0.28, np.array([0.005, 0.0075]), 0), [0.0764274396173414, 0.0248877718180402])
