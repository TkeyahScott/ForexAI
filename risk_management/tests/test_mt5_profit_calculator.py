
# ==========================================
# FOREXAI: MT5 PROFIT CALCULATOR TEST
# ==========================================

import unittest
import MetaTrader5 as mt5

from risk_management.mt5_profit_calculator import (
    calculate_mt5_loss_per_lot,
    calculate_mt5_projected_loss
)
from unittest.mock import patch

class TestMT5ProfitCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if not mt5.initialize():
            raise RuntimeError(
                f"MT5 initialization failed: {mt5.last_error()}"
            )

    @classmethod
    def tearDownClass(cls):
        mt5.shutdown()

    def test_eurusd_buy_loss(self):
        result = calculate_mt5_loss_per_lot(
            symbol="EURUSD",
            direction="BUY",
            entry_price=1.15000,
            stop_loss=1.14900
        )

        self.assertLess(result["projected_profit"], 0)
        self.assertGreater(result["loss_per_lot"], 0)
        self.assertEqual(result["direction"], "BUY")

        print("\n=== EURUSD BUY LOSS ===")
        print(result)

    def test_eurusd_sell_loss(self):
        result = calculate_mt5_loss_per_lot(
            symbol="EURUSD",
            direction="SELL",
            entry_price=1.15000,
            stop_loss=1.15100
        )

        self.assertLess(result["projected_profit"], 0)
        self.assertGreater(result["loss_per_lot"], 0)
        self.assertEqual(result["direction"], "SELL")

        print("\n=== EURUSD SELL LOSS ===")
        print(result)

    def test_invalid_direction(self):
        with self.assertRaises(ValueError):
            calculate_mt5_loss_per_lot(
                symbol="EURUSD",
                direction="HOLD",
                entry_price=1.15000,
                stop_loss=1.14900
            )


    def test_rejects_zero_volume(self):
        """Reject a position volume of zero."""

        with self.assertRaises(ValueError):
            calculate_mt5_projected_loss(
                symbol="EURUSD",
                direction="BUY",
                volume=0,
                entry_price=1.15000,
                stop_loss=1.14900
            )

    def test_rejects_negative_volume(self):
        """Reject a negative position volume."""

        with self.assertRaises(ValueError):
            calculate_mt5_projected_loss(
                symbol="EURUSD",
                direction="BUY",
                volume=-0.10,
                entry_price=1.15000,
                stop_loss=1.14900
            )


    def test_rejects_zero_projected_profit(self):
        """Reject a projected result of zero."""

        with patch(
            "risk_management.mt5_profit_calculator.mt5.symbol_select",
            return_value=True
        ), patch(
            "risk_management.mt5_profit_calculator.mt5.order_calc_profit",
            return_value=0.0
        ):
            with self.assertRaises(ValueError):
                calculate_mt5_projected_loss(
                    symbol="EURUSD",
                    direction="BUY",
                    volume=0.10,
                    entry_price=1.15000,
                    stop_loss=1.14900
                )


    def test_rejects_positive_projected_profit(self):
        """Reject a projected result that represents a profit."""

        with patch(
            "risk_management.mt5_profit_calculator.mt5.symbol_select",
            return_value=True
        ), patch(
            "risk_management.mt5_profit_calculator.mt5.order_calc_profit",
            return_value=10.0
        ):
            with self.assertRaises(ValueError):
                calculate_mt5_projected_loss(
                    symbol="EURUSD",
                    direction="BUY",
                    volume=0.10,
                    entry_price=1.15000,
                    stop_loss=1.14900
                )


if __name__ == "__main__":
    unittest.main()
