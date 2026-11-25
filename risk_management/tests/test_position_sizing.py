
# ==========================================
# FOREXAI: POSITION SIZING TESTS
# ==========================================

import unittest

from risk_management.position_sizing import (
    calculate_position_size,
    adjust_position_size_to_broker
)


class TestPositionSizing(unittest.TestCase):

    # --------------------------------------
    # TEST DEFAULT 1% RISK
    # --------------------------------------

    def test_default_risk_percentage(self):

        result = calculate_position_size(
            account_balance=1000,
            entry_price=1.1000,
            stop_loss=1.0985,
            tick_size=0.0001,
            tick_value=1.0
        )

        self.assertEqual(
            result["risk_percentage"], 1.0
        )

        self.assertAlmostEqual(
            result["risk_amount"], 10.0
        )

    # --------------------------------------
    # TEST CUSTOM RISK PERCENTAGE
    # --------------------------------------

    def test_custom_risk_percentage(self):

        result = calculate_position_size(
            account_balance=1000,
            entry_price=1.1000,
            stop_loss=1.0985,
            tick_size=0.0001,
            tick_value=1.0,
            risk_percentage=2.0
        )

        self.assertAlmostEqual(
            result["risk_amount"], 20.0
        )

    # --------------------------------------
    # TEST POSITION SIZE
    # --------------------------------------

    def test_position_size_calculation(self):

        result = calculate_position_size(
            account_balance=1000,
            entry_price=1.1000,
            stop_loss=1.0985,
            tick_size=0.0001,
            tick_value=1.0
        )

        self.assertAlmostEqual(
            result["position_size"], 0.6666666667
        )

    # --------------------------------------
    # TEST RISK PER LOT
    # --------------------------------------

    def test_risk_per_lot(self):

        result = calculate_position_size(
            account_balance=1000,
            entry_price=1.1000,
            stop_loss=1.0985,
            tick_size=0.0001,
            tick_value=1.0
        )

        self.assertAlmostEqual(
            result["risk_per_lot"], 15.0
        )

    # --------------------------------------
    # TEST INVALID ACCOUNT BALANCE
    # --------------------------------------

    def test_invalid_account_balance(self):

        with self.assertRaises(ValueError):

            calculate_position_size(
                account_balance=0,
                entry_price=1.1000,
                stop_loss=1.0985,
                tick_size=0.0001,
                tick_value=1.0
            )

    # --------------------------------------
    # TEST INVALID STOP-LOSS
    # --------------------------------------

    def test_invalid_stop_loss(self):

        with self.assertRaises(ValueError):

            calculate_position_size(
                account_balance=1000,
                entry_price=1.1000,
                stop_loss=1.1000,
                tick_size=0.0001,
                tick_value=1.0
            )

    # --------------------------------------
    # TEST INVALID TICK SIZE
    # --------------------------------------

    def test_invalid_tick_size(self):

        with self.assertRaises(ValueError):

            calculate_position_size(
                account_balance=1000,
                entry_price=1.1000,
                stop_loss=1.0985,
                tick_size=0,
                tick_value=1.0
            )

    # --------------------------------------
    # TEST INVALID TICK VALUE
    # --------------------------------------

    def test_invalid_tick_value(self):

        with self.assertRaises(ValueError):

            calculate_position_size(
                account_balance=1000,
                entry_price=1.1000,
                stop_loss=1.0985,
                tick_size=0.0001,
                tick_value=0
            )

    # --------------------------------------
    # TEST INVALID RISK PERCENTAGE
    # --------------------------------------

    def test_invalid_risk_percentage(self):

        with self.assertRaises(ValueError):

            calculate_position_size(
                account_balance=1000,
                entry_price=1.1000,
                stop_loss=1.0985,
                tick_size=0.0001,
                tick_value=1.0,
                risk_percentage=0
            )


class TestBrokerVolumeAdjustment(unittest.TestCase):

    def test_rounds_volume_down(self):
        result = adjust_position_size_to_broker(
            position_size=0.667,
            volume_min=0.01,
            volume_max=100.0,
            volume_step=0.01
        )
        self.assertEqual(result, 0.66)

    def test_caps_volume_at_maximum(self):
        result = adjust_position_size_to_broker(
            position_size=150.0,
            volume_min=0.01,
            volume_max=100.0,
            volume_step=0.01
        )
        self.assertEqual(result, 100.0)

    def test_rejects_volume_below_minimum(self):
        with self.assertRaises(ValueError):
            adjust_position_size_to_broker(
                position_size=0.005,
                volume_min=0.01,
                volume_max=100.0,
                volume_step=0.01
            )

    def test_accepts_exact_minimum(self):
        result = adjust_position_size_to_broker(
            position_size=0.01,
            volume_min=0.01,
            volume_max=100.0,
            volume_step=0.01
        )
        self.assertEqual(result, 0.01)

    def test_rejects_invalid_volume_step(self):
        with self.assertRaises(ValueError):
            adjust_position_size_to_broker(
                position_size=1.0,
                volume_min=0.01,
                volume_max=100.0,
                volume_step=0
            )

    def test_rejects_maximum_below_minimum(self):
        with self.assertRaises(ValueError):
            adjust_position_size_to_broker(
                position_size=1.0,
                volume_min=1.0,
                volume_max=0.5,
                volume_step=0.01
            )


if __name__ == "__main__":
    unittest.main()
