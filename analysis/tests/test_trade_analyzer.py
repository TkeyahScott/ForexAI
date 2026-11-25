
# ==========================================
# FOREXAI: TRADE ANALYZER TESTS
# ==========================================

# Tests the H4 main trend analysis function.


import unittest
import pandas as pd

from analysis.trade_analyzer import (
    analyze_h4_trend,
    confirm_h1_trend,
    generate_m15_entry_signal
)


class TestH4TrendAnalysis(unittest.TestCase):

    # --------------------------------------
    # TEST BULLISH TREND
    # --------------------------------------

    def test_bullish_trend(self):

        data = pd.DataFrame({
            "close": [1.1050],
            "ema_20": [1.1000],
            "ema_50": [1.0950]
        })

        result = analyze_h4_trend(data)

        self.assertEqual(result, "BULLISH")

    # --------------------------------------
    # TEST BEARISH TREND
    # --------------------------------------

    def test_bearish_trend(self):

        data = pd.DataFrame({
            "close": [1.0850],
            "ema_20": [1.0900],
            "ema_50": [1.0950]
        })

        result = analyze_h4_trend(data)

        self.assertEqual(result, "BEARISH")

    # --------------------------------------
    # TEST NEUTRAL TREND
    # --------------------------------------

    def test_neutral_trend(self):

        data = pd.DataFrame({
            "close": [1.0920],
            "ema_20": [1.0950],
            "ema_50": [1.0900]
        })

        result = analyze_h4_trend(data)

        self.assertEqual(result, "NEUTRAL")

    # --------------------------------------
    # TEST MISSING DATA
    # --------------------------------------

    def test_missing_data(self):

        result = analyze_h4_trend(None)

        self.assertEqual(result, "NEUTRAL")

    # --------------------------------------
    # TEST EMPTY DATAFRAME
    # --------------------------------------

    def test_empty_dataframe(self):

        data = pd.DataFrame()

        result = analyze_h4_trend(data)

        self.assertEqual(result, "NEUTRAL")

    # --------------------------------------
    # TEST MISSING COLUMNS
    # --------------------------------------

    def test_missing_columns(self):

        data = pd.DataFrame({
            "close": [1.1050],
            "ema_20": [1.1000]
        })

        result = analyze_h4_trend(data)

        self.assertEqual(result, "NEUTRAL")

    # --------------------------------------
    # TEST INVALID INDICATOR VALUES
    # --------------------------------------

    def test_invalid_values(self):

        data = pd.DataFrame({
            "close": [float("nan")],
            "ema_20": [1.1000],
            "ema_50": [1.0950]
        })

        result = analyze_h4_trend(data)

        self.assertEqual(result, "NEUTRAL")


# ==========================================
# H1 TREND CONFIRMATION TESTS
# ==========================================

class TestH1TrendConfirmation(unittest.TestCase):

    def test_bullish_h1_confirmation(self):
        data = pd.DataFrame({
            "ema_20": [1.1050],
            "ema_50": [1.1000],
            "rsi_14": [60.0]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "BULLISH"
        )

    def test_bearish_h1_confirmation(self):
        data = pd.DataFrame({
            "ema_20": [1.0950],
            "ema_50": [1.1000],
            "rsi_14": [40.0]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "BEARISH"
        )

    def test_conflicting_conditions_return_neutral(self):
        data = pd.DataFrame({
            "ema_20": [1.1050],
            "ema_50": [1.1000],
            "rsi_14": [45.0]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "NEUTRAL"
        )

    def test_rsi_of_50_returns_neutral(self):
        data = pd.DataFrame({
            "ema_20": [1.1050],
            "ema_50": [1.1000],
            "rsi_14": [50.0]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "NEUTRAL"
        )

    def test_missing_data_returns_neutral(self):
        self.assertEqual(
            confirm_h1_trend(None),
            "NEUTRAL"
        )

    def test_empty_dataframe_returns_neutral(self):
        data = pd.DataFrame()

        self.assertEqual(
            confirm_h1_trend(data),
            "NEUTRAL"
        )

    def test_missing_columns_return_neutral(self):
        data = pd.DataFrame({
            "ema_20": [1.1050],
            "ema_50": [1.1000]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "NEUTRAL"
        )

    def test_nan_values_return_neutral(self):
        data = pd.DataFrame({
            "ema_20": [float("nan")],
            "ema_50": [1.1000],
            "rsi_14": [60.0]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "NEUTRAL"
        )

    def test_rsi_outside_valid_range_returns_neutral(self):
        data = pd.DataFrame({
            "ema_20": [1.1050],
            "ema_50": [1.1000],
            "rsi_14": [105.0]
        })

        self.assertEqual(
            confirm_h1_trend(data),
            "NEUTRAL"
        )
# ==========================================
# M15 ENTRY SIGNAL TESTS
# ==========================================

class TestM15EntrySignal(unittest.TestCase):

    def test_valid_buy_signal(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "high": [1.1060],
            "low": [1.0990],
            "close": [1.1050],
            "ema_20": [1.1020],
            "rsi_14": [60.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BULLISH", "BULLISH"
            ),
            "BUY"
        )

    def test_valid_sell_signal(self):
        data = pd.DataFrame({
            "open": [1.1050],
            "high": [1.1060],
            "low": [1.0990],
            "close": [1.1000],
            "ema_20": [1.1030],
            "rsi_14": [40.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BEARISH", "BEARISH"
            ),
            "SELL"
        )

    def test_conflicting_higher_timeframes_return_no_trade(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "high": [1.1060],
            "low": [1.0990],
            "close": [1.1050],
            "ema_20": [1.1020],
            "rsi_14": [60.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BULLISH", "BEARISH"
            ),
            "NO TRADE"
        )

    def test_neutral_higher_timeframe_returns_no_trade(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "high": [1.1060],
            "low": [1.0990],
            "close": [1.1050],
            "ema_20": [1.1020],
            "rsi_14": [60.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "NEUTRAL", "NEUTRAL"
            ),
            "NO TRADE"
        )

    def test_missing_m15_data_returns_no_trade(self):
        self.assertEqual(
            generate_m15_entry_signal(
                None, "BULLISH", "BULLISH"
            ),
            "NO TRADE"
        )

    def test_empty_m15_dataframe_returns_no_trade(self):
        self.assertEqual(
            generate_m15_entry_signal(
                pd.DataFrame(), "BULLISH", "BULLISH"
            ),
            "NO TRADE"
        )

    def test_missing_columns_return_no_trade(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "close": [1.1050],
            "ema_20": [1.1020]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BULLISH", "BULLISH"
            ),
            "NO TRADE"
        )

    def test_rsi_of_50_returns_no_trade(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "high": [1.1060],
            "low": [1.0990],
            "close": [1.1050],
            "ema_20": [1.1020],
            "rsi_14": [50.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BULLISH", "BULLISH"
            ),
            "NO TRADE"
        )

    def test_invalid_rsi_returns_no_trade(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "high": [1.1060],
            "low": [1.0990],
            "close": [1.1050],
            "ema_20": [1.1020],
            "rsi_14": [105.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BULLISH", "BULLISH"
            ),
            "NO TRADE"
        )

    def test_invalid_candle_structure_returns_no_trade(self):
        data = pd.DataFrame({
            "open": [1.1000],
            "high": [1.1010],
            "low": [1.0990],
            "close": [1.1050],
            "ema_20": [1.1020],
            "rsi_14": [60.0]
        })

        self.assertEqual(
            generate_m15_entry_signal(
                data, "BULLISH", "BULLISH"
            ),
            "NO TRADE"
        )
if __name__ == "__main__":
    unittest.main()