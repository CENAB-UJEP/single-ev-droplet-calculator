from __future__ import annotations

import math
import unittest

from single_ev_droplet_calculator.core import (
    compare_operating_points,
    lambda_confidence_interval_from_empty_counts,
    lambda_from_empty_fraction,
    occupancy_metrics,
    required_droplets_for_target_events,
)


class TestCoreMath(unittest.TestCase):
    def test_anchor_lambda_010(self) -> None:
        m = occupancy_metrics(0.10)
        self.assertAlmostEqual(m.p_empty, 0.9048374180, places=8)
        self.assertAlmostEqual(m.p_single, 0.0904837418, places=8)
        self.assertAlmostEqual(m.p_multi_ge_2, 0.0046788401, places=8)
        self.assertAlmostEqual(m.purity_given_occupied, 0.9508331945, places=8)

    def test_anchor_lambda_020(self) -> None:
        m = occupancy_metrics(0.20)
        self.assertAlmostEqual(m.p_empty, 0.8187307531, places=8)
        self.assertAlmostEqual(m.p_single, 0.1637461506, places=8)
        self.assertAlmostEqual(m.p_multi_ge_2, 0.0175230963, places=8)
        self.assertAlmostEqual(m.purity_given_occupied, 0.9033311132, places=8)

    def test_compare_ratios(self) -> None:
        c = compare_operating_points(0.10, 0.20)
        self.assertAlmostEqual(c.single_yield_ratio_b_over_a, 1.8096748361, places=9)
        self.assertAlmostEqual(c.multi_burden_ratio_b_over_a, 3.7451795115, places=9)

    def test_required_droplets_planning(self) -> None:
        n = required_droplets_for_target_events(
            target_interpretable_single_events=10000,
            lambda_value=0.10,
            q_qc=0.60,
            q_identity=0.70,
        )
        self.assertAlmostEqual(n, 263135.9329, places=3)

    def test_lambda_from_empty(self) -> None:
        f = math.exp(-0.10)
        self.assertAlmostEqual(lambda_from_empty_fraction(f), 0.10, places=10)

    def test_lambda_ci(self) -> None:
        ci = lambda_confidence_interval_from_empty_counts(
            n_empty=9048,
            n_total=10000,
            confidence=0.95,
        )
        self.assertTrue(ci.lower < 0.10 < ci.upper)
        self.assertTrue(ci.lower >= 0)

    def test_invalid_inputs(self) -> None:
        with self.assertRaises(ValueError):
            occupancy_metrics(-0.1)
        with self.assertRaises(ValueError):
            lambda_from_empty_fraction(1.0)
        with self.assertRaises(ValueError):
            required_droplets_for_target_events(1000, 0.1, q_qc=1.2, q_identity=0.9)


if __name__ == "__main__":
    unittest.main()

