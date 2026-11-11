# Test to ensure market data retrieval is functioning correctly.
# Also ensure the Timzones is switched to UTC so that the data is consistent with the MT5 terminal.


# Import the multi-timeframe data collection function.
from data.market_data import get_watchlist_market_data


# ==========================================
# FOREXAI: MULTI-TIMEFRAME DATA TEST
# ==========================================

print("\n=== FOREXAI: MULTI-TIMEFRAME DATA TEST ===\n")

# Request 100 completed candles for every pair and timeframe.
number_of_candles = 100

# Retrieve all watchlist market data.
market_data = get_watchlist_market_data(number_of_candles)


# Check whether the collection function returned data.
if market_data is not None:

    # Track how many datasets were successfully retrieved.
    successful_datasets = 0

    # Track datasets that could not be retrieved.
    failed_datasets = 0

    # These are the three timeframes we expect.
    expected_timeframes = ["M15", "H1", "H4"]

    print("\n=== COLLECTION RESULTS ===\n")

    # Go through every currency pair.
    for symbol, timeframe_data in market_data.items():

        print(f"\nCurrency pair: {symbol}")

        # Check whether the currency pair has usable data.
        if timeframe_data is None:

            print("  All timeframes unavailable.")
            failed_datasets += len(expected_timeframes)
            continue

        # Check each timeframe individually.
        for timeframe in expected_timeframes:

            df = timeframe_data.get(timeframe)

            if df is not None:

                successful_datasets += 1

                print(f"\n  Timeframe: {timeframe}")
                print(f"  Candles retrieved: {len(df)}")
                print(f"  Latest completed candle: {df['time'].iloc[-1]}")

            else:

                failed_datasets += 1
                print(f"\n  Timeframe: {timeframe}")
                print("  Data unavailable.")

    # Display the overall collection summary.
    total_datasets = successful_datasets + failed_datasets

    print("\n=== FINAL TEST SUMMARY ===")

    print("Expected datasets:", total_datasets)
    print("Successful datasets:", successful_datasets)
    print("Failed datasets:", failed_datasets)

    # Confirm whether all 24 combinations were retrieved.
    if successful_datasets == 24:

        print("\nFOREXAI MULTI-TIMEFRAME TEST PASSED!")

    else:

        print("\nFOREXAI MULTI-TIMEFRAME TEST INCOMPLETE.")
        print("Review any unavailable datasets above.")

else:

    print("\nFOREXAI MULTI-TIMEFRAME TEST FAILED!")
    print("Could not retrieve market data from MT5.")
