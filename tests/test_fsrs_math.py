import unittest

from fsrs_math import (
    interval_for_target_retrievability,
    power_forgetting_curve,
    fsrs7_forgetting_curve,
)


class TestFsrsMath(unittest.TestCase):
    def test_interval_for_90_percent_matches_stability_for_scalar_decay(self):
        stability = 25.0
        s90 = interval_for_target_retrievability(
            stability=stability,
            desired_retention=0.9,
            decay=-0.5,
        )
        self.assertEqual(s90, 25)
        self.assertAlmostEqual(power_forgetting_curve(s90, stability, -0.5), 0.9, places=6)

    def test_interval_for_90_percent_differs_from_stability_for_fsrs7(self):
        params = [0.0] * 35
        params[27] = 0.6
        params[28] = 1.1
        params[29] = 0.86
        params[30] = 0.95
        params[31] = 1.2
        params[32] = 0.7
        params[33] = 0.2
        params[34] = 0.15

        stability = 10.0
        s90 = interval_for_target_retrievability(
            stability=stability,
            desired_retention=0.9,
            params=params,
        )

        self.assertNotEqual(s90, round(stability))
        r_at_s90 = fsrs7_forgetting_curve(s90, stability, params)
        r_prev = fsrs7_forgetting_curve(max(1, s90 - 1), stability, params)
        r_next = fsrs7_forgetting_curve(s90 + 1, stability, params)
        self.assertLessEqual(abs(r_at_s90 - 0.9), abs(r_prev - 0.9))
        self.assertLessEqual(abs(r_at_s90 - 0.9), abs(r_next - 0.9))


if __name__ == "__main__":
    unittest.main()
