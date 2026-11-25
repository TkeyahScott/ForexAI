# ==========================================
# FOREXAI: MT5 RISK DATA TEST
# ==========================================

import unittest
import MetaTrader5 as mt5

from risk_management.mt5_risk_data import get_mt5_risk_data


class TestMTRiskData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to MT5 once for the test session.
        if not mt5.initialize():
            raise RuntimeError(
                f"MT5 initialization failed: {mt5.last_error()}"
            )

    @classmethod
    def tearDownClass(cls):
        # Close the connection after testing.
        mt5.shutdown()

    def test_retrieve_eurusd_risk_data(self):
        result = get_mt5_risk_data("EURUSD")

        self.assertEqual(result["symbol"], "EURUSD")
        self.assertGreater(result["account_balance"], 0)
        self.assertTrue(result["account_currency"])
        self.assertGreater(result["tick_size"], 0)
        self.assertGreater(result["tick_value"], 0)
        self.assertGreater(result["volume_min"], 0)
        self.assertGreater(result["volume_max"], 0)
        self.assertGreater(result["volume_step"], 0)

        print("\n=== MT5 RISK DATA ===")

        for field, value in result.items():
            print(f"{field}: {value}")


if __name__ == "__main__":
    unittest.main()