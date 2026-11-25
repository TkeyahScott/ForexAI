
# ==========================================
# FOREXAI: RISK CALCULATOR TESTS
# ==========================================

import unittest

from risk_management.risk_calculator import (
    calculate_stop_loss_take_profit
)


class TestRiskCalculator(unittest.TestCase):

    # --------------------------------------
    # TEST BUY CALCULATION
    # --------------------------------------

    def test_buy_calculation(self):

        result = calculate_stop_loss_take_profit(
            entry_price=1.1000,
            direction="BUY",
            atr=0.0010
        )

        self.assertAlmostEqual(
            result["stop_loss"], 1.0985
        )

        self.assertAlmostEqual(
            result["take_profit"], 1.1030
        )

    # --------------------------------------
    # TEST SELL CALCULATION
    # --------------------------------------

    def test_sell_calculation(self):

        result = calculate_stop_loss_take_profit(
            entry_price=1.1000,
            direction="SELL",
            atr=0.0010
        )

        self.assertAlmostEqual(
            result["stop_loss"], 1.1015
        )

        self.assertAlmostEqual(
            result["take_profit"], 1.0970
        )

    # --------------------------------------
    # TEST STOP-LOSS DISTANCE
    # --------------------------------------

    def test_stop_loss_distance(self):

        result = calculate_stop_loss_take_profit(
            entry_price=1.1000,
            direction="BUY",
            atr=0.0010
        )

        self.assertAlmostEqual(
            result["stop_distance"], 0.0015
        )

    # --------------------------------------
    # TEST REWARD DISTANCE
    # --------------------------------------

    def test_reward_distance(self):

        result = calculate_stop_loss_take_profit(
            entry_price=1.1000,
            direction="BUY",
            atr=0.0010
        )

        self.assertAlmostEqual(
            result["reward_distance"], 0.0030
        )

    # --------------------------------------
    # TEST RISK/REWARD RATIO
    # --------------------------------------

    def test_risk_reward_ratio(self):

        result = calculate_stop_loss_take_profit(
            entry_price=1.1000,
            direction="BUY",
            atr=0.0010
        )

        self.assertEqual(
            result["risk_reward_ratio"], 2.0
        )

    # --------------------------------------
    # TEST INVALID DIRECTION
    # --------------------------------------

    def test_invalid_direction(self):

        with self.assertRaises(ValueError):

            calculate_stop_loss_take_profit(
                entry_price=1.1000,
                direction="HOLD",
                atr=0.0010
            )

    # --------------------------------------
    # TEST ZERO ATR
    # --------------------------------------

    def test_zero_atr(self):

        with self.assertRaises(ValueError):

            calculate_stop_loss_take_profit(
                entry_price=1.1000,
                direction="BUY",
                atr=0
            )

    # --------------------------------------
    # TEST NEGATIVE ATR
    # --------------------------------------

    def test_negative_atr(self):

        with self.assertRaises(ValueError):

            calculate_stop_loss_take_profit(
                entry_price=1.1000,
                direction="BUY",
                atr=-0.0010
            )

    # --------------------------------------
    # TEST INVALID ENTRY PRICE
    # --------------------------------------

    def test_invalid_entry_price(self):

        with self.assertRaises(ValueError):

            calculate_stop_loss_take_profit(
                entry_price=0,
                direction="BUY",
                atr=0.0010
            )

    # --------------------------------------
    # TEST INVALID STOP MULTIPLIER
    # --------------------------------------

    def test_invalid_stop_multiplier(self):

        with self.assertRaises(ValueError):

            calculate_stop_loss_take_profit(
                entry_price=1.1000,
                direction="BUY",
                atr=0.0010,
                stop_multiplier=0
            )


if __name__ == "__main__":
    unittest.main()
