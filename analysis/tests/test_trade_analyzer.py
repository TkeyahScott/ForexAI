
# ==========================================
# FOREXAI: TRADE ANALYZER TESTS
# ==========================================

# Tests the H4 main trend analysis function.


import unittest
import pandas as pd

from analysis.trade_analyzer import (
    analyze_h4_trend,
    analyze_market,
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


    # --------------------------------------
    # TEST INFINITE VALUES
    # --------------------------------------

    def test_infinite_values(self):

        # Each H4 price and EMA value must be finite.
        for column in ["close", "ema_20", "ema_50"]:

            with self.subTest(column=column):

                values = {
                    "close": 1.1050,
                    "ema_20": 1.1000,
                    "ema_50": 1.0950
                }

                values[column] = float("inf")

                data = pd.DataFrame([values])

                self.assertEqual(
                    analyze_h4_trend(data),
                    "NEUTRAL"
                )

    # --------------------------------------
    # TEST ZERO AND NEGATIVE PRICES
    # --------------------------------------

    def test_non_positive_prices(self):

        # All H4 prices and EMA values must be positive.
        for column in ["close", "ema_20", "ema_50"]:

            for invalid_value in [0, -1]:

                with self.subTest(
                    column=column,
                    value=invalid_value
                ):

                    values = {
                        "close": 1.1050,
                        "ema_20": 1.1000,
                        "ema_50": 1.0950
                    }

                    values[column] = invalid_value

                    data = pd.DataFrame([values])

                    self.assertEqual(
                        analyze_h4_trend(data),
                        "NEUTRAL"
                    )

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


    # --------------------------------------
    # TEST INFINITE VALUES
    # --------------------------------------

    def test_infinite_values_return_neutral(self):

        # EMA and RSI values must all be finite.
        for column in ["ema_20", "ema_50", "rsi_14"]:

            with self.subTest(column=column):

                values = {
                    "ema_20": 1.1050,
                    "ema_50": 1.1000,
                    "rsi_14": 60.0
                }

                values[column] = float("inf")

                data = pd.DataFrame([values])

                self.assertEqual(
                    confirm_h1_trend(data),
                    "NEUTRAL"
                )

    # --------------------------------------
    # TEST NON-POSITIVE EMAS AND INVALID RSI
    # --------------------------------------

    def test_invalid_numeric_ranges_return_neutral(self):

        # EMA values must be positive.
        for column in ["ema_20", "ema_50"]:

            for invalid_value in [0, -1]:

                with self.subTest(
                    column=column,
                    value=invalid_value
                ):

                    values = {
                        "ema_20": 1.1050,
                        "ema_50": 1.1000,
                        "rsi_14": 60.0
                    }

                    values[column] = invalid_value

                    data = pd.DataFrame([values])

                    self.assertEqual(
                        confirm_h1_trend(data),
                        "NEUTRAL"
                    )

        # RSI must remain between 0 and 100.
        for invalid_value in [-1, float("inf")]:

            with self.subTest(rsi=invalid_value):

                data = pd.DataFrame({
                    "ema_20": [1.1050],
                    "ema_50": [1.1000],
                    "rsi_14": [invalid_value]
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


    # --------------------------------------
    # TEST INFINITE VALUES
    # --------------------------------------

    def test_infinite_values_return_no_trade(self):

        # Every price and indicator must be finite.
        for column in [
            "open",
            "high",
            "low",
            "close",
            "ema_20",
            "rsi_14"
        ]:

            with self.subTest(column=column):

                values = {
                    "open": 1.1000,
                    "high": 1.1060,
                    "low": 1.0990,
                    "close": 1.1050,
                    "ema_20": 1.1020,
                    "rsi_14": 60.0
                }

                values[column] = float("inf")

                data = pd.DataFrame([values])

                self.assertEqual(
                    generate_m15_entry_signal(
                        data, "BULLISH", "BULLISH"
                    ),
                    "NO TRADE"
                )

    # --------------------------------------
    # TEST NON-POSITIVE PRICES AND INVALID RSI
    # --------------------------------------

    def test_invalid_numeric_ranges_return_no_trade(self):

        # All candle prices and EMA20 must be positive.
        for column in [
            "open",
            "high",
            "low",
            "close",
            "ema_20"
        ]:

            for invalid_value in [0, -1]:

                with self.subTest(
                    column=column,
                    value=invalid_value
                ):

                    values = {
                        "open": 1.1000,
                        "high": 1.1060,
                        "low": 1.0990,
                        "close": 1.1050,
                        "ema_20": 1.1020,
                        "rsi_14": 60.0
                    }

                    values[column] = invalid_value

                    data = pd.DataFrame([values])

                    self.assertEqual(
                        generate_m15_entry_signal(
                            data, "BULLISH", "BULLISH"
                        ),
                        "NO TRADE"
                    )

        # RSI must remain between 0 and 100.
        for invalid_value in [-1, float("inf")]:

            with self.subTest(rsi=invalid_value):

                data = pd.DataFrame({
                    "open": [1.1000],
                    "high": [1.1060],
                    "low": [1.0990],
                    "close": [1.1050],
                    "ema_20": [1.1020],
                    "rsi_14": [invalid_value]
                })

                self.assertEqual(
                    generate_m15_entry_signal(
                        data, "BULLISH", "BULLISH"
                    ),
                    "NO TRADE"
                )

    def test_analyze_market_returns_all_three_results(self):
        h4_data = pd.DataFrame({
            "close": [1.1050],
            "ema_20": [1.1030],
            "ema_50": [1.1000]
        })

        h1_data = pd.DataFrame({
            "ema_20": [1.1040],
            "ema_50": [1.1010],
            "rsi_14": [60.0]
        })

        m15_data = pd.DataFrame({
            "open": [1.1030],
            "high": [1.1060],
            "low": [1.1020],
            "close": [1.1050],
            "ema_20": [1.1040],
            "rsi_14": [60.0]
        })

        result = analyze_market(
            h4_data,
            h1_data,
            m15_data
        )

        self.assertEqual(
            result,
            {
                "h4_trend": "BULLISH",
                "h1_trend": "BULLISH",
                "entry_signal": "BUY"
            }
        )

    def test_analyze_market_returns_sell_signal(self):
        h4_data = pd.DataFrame({
            "close": [1.0950],
            "ema_20": [1.0970],
            "ema_50": [1.1000]
        })

        h1_data = pd.DataFrame({
            "ema_20": [1.0960],
            "ema_50": [1.0990],
            "rsi_14": [40.0]
        })

        m15_data = pd.DataFrame({
            "open": [1.0970],
            "high": [1.0980],
            "low": [1.0940],
            "close": [1.0950],
            "ema_20": [1.0960],
            "rsi_14": [40.0]
        })

        result = analyze_market(
            h4_data,
            h1_data,
            m15_data
        )

        self.assertEqual(
            result,
            {
                "h4_trend": "BEARISH",
                "h1_trend": "BEARISH",
                "entry_signal": "SELL"
            }
        )

    def test_analyze_market_returns_no_trade_when_trends_conflict(self):
        h4_data = pd.DataFrame({
            "close": [1.1050],
            "ema_20": [1.1030],
            "ema_50": [1.1000]
        })

        h1_data = pd.DataFrame({
            "ema_20": [1.0970],
            "ema_50": [1.1000],
            "rsi_14": [40.0]
        })

        m15_data = pd.DataFrame({
            "open": [1.1030],
            "high": [1.1060],
            "low": [1.1020],
            "close": [1.1050],
            "ema_20": [1.1040],
            "rsi_14": [60.0]
        })

        result = analyze_market(
            h4_data,
            h1_data,
            m15_data
        )

        self.assertEqual(
            result,
            {
                "h4_trend": "BULLISH",
                "h1_trend": "BEARISH",
                "entry_signal": "NO TRADE"
            }
        )

    def test_analyze_market_returns_no_trade_when_h4_data_missing(self):
        h1_data = pd.DataFrame({
            "ema_20": [1.1040],
            "ema_50": [1.1010],
            "rsi_14": [60.0]
        })

        m15_data = pd.DataFrame({
            "open": [1.1030],
            "high": [1.1060],
            "low": [1.1020],
            "close": [1.1050],
            "ema_20": [1.1040],
            "rsi_14": [60.0]
        })

        result = analyze_market(
            None,
            h1_data,
            m15_data
        )

        self.assertEqual(
            result,
            {
                "h4_trend": "NEUTRAL",
                "h1_trend": "BULLISH",
                "entry_signal": "NO TRADE"
            }
        )



if __name__ == "__main__":
    unittest.main()
