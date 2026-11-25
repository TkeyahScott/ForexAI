
# ==========================================
# FOREXAI: MT5 POSITION SIZING TEST
# ==========================================

import unittest
import MetaTrader5 as mt5

from risk_management.mt5_position_sizing import (
    calculate_mt5_position_size
)

from unittest.mock import patch

class TestMT5PositionSizing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not mt5.initialize():
            raise RuntimeError(
                f"MT5 initialization failed: {mt5.last_error()}"
            )

    @classmethod
    def tearDownClass(cls):
        mt5.shutdown()

    def test_eurusd_buy_position_sizing(self):
        result = calculate_mt5_position_size(
            symbol="EURUSD",
            direction="BUY",
            entry_price=1.15000,
            stop_loss=1.14900
        )

        self.assertEqual(result["direction"], "BUY")
        self.assertAlmostEqual(result["risk_amount"], 30.0)
        self.assertAlmostEqual(result["loss_per_lot"], 100.0)
        self.assertAlmostEqual(result["position_size"], 0.30)
        self.assertAlmostEqual(result["projected_trade_loss"], 30.0)

        print("\n=== EURUSD BUY POSITION SIZING ===")

        for field, value in result.items():
            print(f"{field}: {value}")

    def test_eurusd_sell_position_sizing(self):
        result = calculate_mt5_position_size(
            symbol="EURUSD",
            direction="SELL",
            entry_price=1.15000,
            stop_loss=1.15100
        )

        self.assertEqual(result["direction"], "SELL")
        self.assertAlmostEqual(result["risk_amount"], 30.0)
        self.assertAlmostEqual(result["loss_per_lot"], 100.0)
        self.assertAlmostEqual(result["position_size"], 0.30)
        self.assertAlmostEqual(result["projected_trade_loss"], 30.0)

        print("\n=== EURUSD SELL POSITION SIZING ===")

        for field, value in result.items():
            print(f"{field}: {value}")



    def test_custom_risk_percentage(self):
        result = calculate_mt5_position_size(
            symbol="EURUSD",
            direction="BUY",
            entry_price=1.15000,
            stop_loss=1.14900,
            risk_percentage=2.0
        )

        self.assertAlmostEqual(result["risk_percentage"], 2.0)
        self.assertAlmostEqual(result["risk_amount"], 60.0)
        self.assertAlmostEqual(result["position_size"], 0.60)
        self.assertAlmostEqual(result["projected_trade_loss"], 60.0)

    def test_rejects_volume_below_broker_minimum(self):
        with self.assertRaises(ValueError):
            calculate_mt5_position_size(
                symbol="EURUSD",
                direction="BUY",
                entry_price=1.15000,
                stop_loss=1.10000
            )

    def test_rejects_invalid_direction(self):
        with self.assertRaises(ValueError):
            calculate_mt5_position_size(
                symbol="EURUSD",
                direction="HOLD",
                entry_price=1.15000,
                stop_loss=1.14900
            )

    def test_caps_volume_at_broker_maximum(self):
        result = calculate_mt5_position_size(
            symbol="EURUSD",
            direction="BUY",
            entry_price=1.15000,
            stop_loss=1.14999,
            risk_percentage=100.0
        )

        self.assertEqual(result["position_size"], 500.0)

        self.assertLessEqual(
            result["projected_trade_loss"],
            result["risk_amount"]
        )


    def test_rejects_projected_loss_above_risk_amount(self):
        """Reject a position when MT5 projected loss exceeds allowed risk."""

        with patch(
            "risk_management.mt5_position_sizing.get_mt5_risk_data"
        ) as mock_risk_data, patch(
            "risk_management.mt5_position_sizing.calculate_mt5_loss_per_lot"
        ) as mock_loss_per_lot, patch(
            "risk_management.mt5_position_sizing.adjust_position_size_to_broker"
        ) as mock_adjust_volume, patch(
            "risk_management.mt5_position_sizing.calculate_mt5_projected_loss"
        ) as mock_final_loss:

            mock_risk_data.return_value = {
                "account_balance": 3000.0,
                "account_currency": "USD",
                "volume_min": 0.01,
                "volume_max": 500.0,
                "volume_step": 0.01
            }

            mock_loss_per_lot.return_value = {
                "direction": "BUY",
                "loss_per_lot": 100.0
            }

            mock_adjust_volume.return_value = 0.30

            mock_final_loss.return_value = {
                "projected_trade_loss": 35.0
            }

            with self.assertRaises(ValueError):
                calculate_mt5_position_size(
                    symbol="EURUSD",
                    direction="BUY",
                    entry_price=1.15000,
                    stop_loss=1.14900
                )


if __name__ == "__main__":
    unittest.main()
