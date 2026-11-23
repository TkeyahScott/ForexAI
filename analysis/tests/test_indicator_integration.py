
# ==========================================
# FOREXAI: INDICATOR INTEGRATION TEST
# ==========================================

# Tests the connection between the Market Data Engine
# and the Technical Indicator Pipeline.


import pandas as pd

from data.market_data import get_watchlist_market_data

from analysis.indicator_pipeline import process_market_data


# ==========================================
# EXPECTED INDICATOR COLUMNS
# ==========================================

EXPECTED_INDICATORS = [
    "ema_20",
    "ema_50",
    "rsi_14",
    "atr_14"
]


# ==========================================
# EXPECTED MARKET DATA STRUCTURE
# ==========================================

EXPECTED_SYMBOLS = [
    "EURUSD",
    "USDJPY",
    "GBPUSD",
    "EURJPY",
    "GBPJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF"
]

EXPECTED_TIMEFRAMES = [
    "M15",
    "H1",
    "H4"
]



# ==========================================
# LIVE MARKET DATA INTEGRATION TEST
# ==========================================

def test_live_indicator_integration():

    print("\nStarting ForexAI indicator integration test...")

    # --------------------------------------
    # STEP 1: Retrieve live market data
    # --------------------------------------

    print("\nRetrieving live MT5 market data...")

    market_data = get_watchlist_market_data()

    # Stop if the MT5 connection or data retrieval failed.
    if market_data is None:
        raise RuntimeError(
            "Market data retrieval failed. "
            "Check that MT5 is open and connected to your broker."
        )

    print("Market data retrieved successfully.")

    # --------------------------------------
    # STEP 2: Process the market data
    # --------------------------------------

    print("\nCalculating technical indicators...")

    processed_data = process_market_data(market_data)

    if processed_data is None:
        raise RuntimeError(
            "The indicator pipeline returned no processed data."
        )

    print("Indicator pipeline completed.")

    # --------------------------------------
    # STEP 3: Verify symbols and timeframes
    # --------------------------------------

    print("\nChecking available market datasets...")

    successful_datasets = 0
    skipped_datasets = 0

    for symbol in EXPECTED_SYMBOLS:

        if symbol not in processed_data:
            print(f"WARNING: {symbol} is missing.")
            continue

        for timeframe in EXPECTED_TIMEFRAMES:

            dataframe = processed_data[symbol].get(timeframe)

            # Some broker datasets may be unavailable.
            if dataframe is None:
                print(f"SKIPPED: {symbol} {timeframe} - no data.")
                skipped_datasets += 1
                continue

            # Confirm that the result is a DataFrame.
            if not isinstance(dataframe, pd.DataFrame):
                raise TypeError(
                    f"{symbol} {timeframe} is not a Pandas DataFrame."
                )

            # ----------------------------------
            # STEP 4: Verify indicator columns
            # ----------------------------------

            missing_indicators = [
                indicator
                for indicator in EXPECTED_INDICATORS
                if indicator not in dataframe.columns
            ]

            if missing_indicators:
                raise AssertionError(
                    f"{symbol} {timeframe} is missing indicators: "
                    f"{missing_indicators}"
                )

                        # ----------------------------------
            # STEP 4B: Verify indicator values
            # ----------------------------------

            # Ensure every indicator contains at least
            # one valid numerical result.
            for indicator in EXPECTED_INDICATORS:

                if not pd.api.types.is_numeric_dtype(
                    dataframe[indicator]
                ):
                    raise AssertionError(
                        f"{symbol} {timeframe}: "
                        f"{indicator} contains non-numeric data."
                    )

                if dataframe[indicator].notna().sum() == 0:
                    raise AssertionError(
                        f"{symbol} {timeframe}: "
                        f"{indicator} contains no valid values."
                    )

            # ----------------------------------
            # STEP 5: Verify original candle data
            # ----------------------------------

            original_columns = [
                "time",
                "open",
                "high",
                "low",
                "close",
                "tick_volume",
                "spread",
                "real_volume"
            ]

            missing_columns = [
                column
                for column in original_columns
                if column not in dataframe.columns
            ]

            if missing_columns:
                raise AssertionError(
                    f"{symbol} {timeframe} is missing original columns: "
                    f"{missing_columns}"
                )

            successful_datasets += 1

            print(
                f"PASSED: {symbol} {timeframe} - "
                f"all four indicators verified."
            )

    # --------------------------------------
    # STEP 6: Display integration summary
    # --------------------------------------

    print("\n==========================================")
    print("INDICATOR INTEGRATION TEST SUMMARY")
    print("==========================================")

    print(f"Successfully processed datasets: {successful_datasets}")
    print(f"Skipped unavailable datasets: {skipped_datasets}")

    if successful_datasets == 0:
        raise AssertionError(
            "No datasets were successfully processed."
        )

    print("\nLIVE INDICATOR INTEGRATION TEST PASSED.")



# ==========================================
# TEST EXECUTION
# ==========================================

if __name__ == "__main__":

    # Run the live integration test only when
    # this file is executed directly as a module.

    try:
        test_live_indicator_integration()

    except Exception as error:

        print("\nLIVE INDICATOR INTEGRATION TEST FAILED.")
        print(f"Reason: {error}")

        # Preserve the error details for troubleshooting.
        raise
6