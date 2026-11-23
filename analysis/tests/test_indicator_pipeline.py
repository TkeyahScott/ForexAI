
# ==========================================
# FOREXAI: INDICATOR PIPELINE TESTS
# ==========================================

import unittest
import numpy as np
import pandas as pd

from analysis.indicator_pipeline import (
    add_technical_indicators,
    process_market_data
)


# ==========================================
# TEST DATA GENERATOR
# ==========================================

def create_test_market_data(number_of_candles=100):
    """
    Generate synthetic OHLC market data.

    This allows us to test the indicator pipeline
    without connecting to MetaTrader 5.
    """

    # Generate a predictable series of closing prices.
    close_prices = (
        100
        + np.linspace(0, 10, number_of_candles)
        + np.sin(np.arange(number_of_candles) / 3)
    )

    # Create realistic high and low values around each close.
    return pd.DataFrame({
        "open": close_prices - 0.1,
        "high": close_prices + 0.5,
        "low": close_prices - 0.5,
        "close": close_prices,
        "tick_volume": np.full(number_of_candles, 100),
    })


# ==========================================
# INDICATOR PIPELINE TESTS
# ==========================================

class TestIndicatorPipeline(unittest.TestCase):

    # --------------------------------------
    # TEST 1: INDICATOR COLUMNS
    # --------------------------------------

    def test_indicator_columns_are_added(self):

        market_data = create_test_market_data()

        result = add_technical_indicators(market_data)

        expected_columns = [
            "ema_20",
            "ema_50",
            "rsi_14",
            "atr_14"
        ]

        for column in expected_columns:
            self.assertIn(column, result.columns)

    # --------------------------------------
    # TEST 2: ORIGINAL DATA IS PRESERVED
    # --------------------------------------

    def test_original_market_data_is_unchanged(self):

        market_data = create_test_market_data()

        original_data = market_data.copy(deep=True)

        add_technical_indicators(market_data)

        pd.testing.assert_frame_equal(
            market_data,
            original_data
        )

    # --------------------------------------
    # TEST 3: INDICATORS PRODUCE VALUES
    # --------------------------------------

    def test_indicators_produce_valid_values(self):

        market_data = create_test_market_data()

        result = add_technical_indicators(market_data)

        # Each indicator should eventually produce
        # at least one calculated value.
        indicator_columns = [
            "ema_20",
            "ema_50",
            "rsi_14",
            "atr_14"
        ]

        for column in indicator_columns:
            self.assertTrue(
                result[column].notna().any(),
                f"{column} did not produce any values."
            )

        # RSI must remain between 0 and 100.
        valid_rsi = result["rsi_14"].dropna()

        self.assertTrue((valid_rsi >= 0).all())
        self.assertTrue((valid_rsi <= 100).all())

        # ATR must be positive for this test dataset.
        valid_atr = result["atr_14"].dropna()

        self.assertTrue((valid_atr > 0).all())

    # --------------------------------------
    # TEST 4: MISSING DATA
    # --------------------------------------

    def test_missing_dataset_returns_none(self):

        result = add_technical_indicators(None)

        self.assertIsNone(result)

    # --------------------------------------
    # TEST 5: INSUFFICIENT CANDLES
    # --------------------------------------

    def test_insufficient_candles_raise_error(self):

        market_data = create_test_market_data(30)

        with self.assertRaises(ValueError):
            add_technical_indicators(market_data)

    # --------------------------------------
    # TEST 6: REQUIRED COLUMNS
    # --------------------------------------

    def test_missing_required_columns_raise_error(self):

        market_data = create_test_market_data()

        market_data = market_data.drop(columns=["high"])

        with self.assertRaises(ValueError):
            add_technical_indicators(market_data)

    # --------------------------------------
    # TEST 7: INVALID INPUT TYPE
    # --------------------------------------

    def test_invalid_input_type_raises_error(self):

        # A dictionary is not a valid market DataFrame.
        invalid_data = {"close": [1.0, 2.0, 3.0]}

        with self.assertRaises(TypeError):
            add_technical_indicators(invalid_data)


    # --------------------------------------
    # TEST 8: MULTI-TIMEFRAME PROCESSING
    # --------------------------------------

    def test_multiple_timeframes_are_processed(self):

        market_data = {
            "EURUSD": {
                "M15": create_test_market_data(),
                "H1": create_test_market_data(),
                "H4": create_test_market_data()
            }
        }

        result = process_market_data(market_data)

        for timeframe in ["M15", "H1", "H4"]:

            self.assertIn(
                "ema_20",
                result["EURUSD"][timeframe].columns
            )

            self.assertIn(
                "ema_50",
                result["EURUSD"][timeframe].columns
            )

            self.assertIn(
                "rsi_14",
                result["EURUSD"][timeframe].columns
            )

            self.assertIn(
                "atr_14",
                result["EURUSD"][timeframe].columns
            )

    # --------------------------------------
    # TEST 9: UNAVAILABLE DATA IS PRESERVED
    # --------------------------------------

    def test_missing_timeframe_is_preserved(self):

        market_data = {
            "EURUSD": {
                "M15": create_test_market_data(),
                "H1": None,
                "H4": create_test_market_data()
            },
            "GBPUSD": None
        }

        result = process_market_data(market_data)

        self.assertIsNone(result["EURUSD"]["H1"])
        self.assertIsNone(result["GBPUSD"])


# ==========================================
# RUN TESTS
# ==========================================

if __name__ == "__main__":
    unittest.main()
