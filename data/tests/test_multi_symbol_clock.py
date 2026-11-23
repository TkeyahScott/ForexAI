
# Import tools for timestamp comparison.
import time
from datetime import datetime, timezone

# Import MetaTrader 5.
import MetaTrader5 as mt5


# ==========================================
# FOREXAI: MULTI-SYMBOL CLOCK TEST
# ==========================================

# The eight currency pairs in our ForexAI watchlist.
WATCHLIST = [
    "EURUSD",
    "USDJPY",
    "GBPUSD",
    "EURJPY",
    "GBPJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF",
]

print("\n=== FOREXAI: MULTI-SYMBOL CLOCK TEST ===\n")

# Connect to the running MT5 terminal.
if not mt5.initialize():

    print("MT5 connection failed:", mt5.last_error())

else:

    try:
        # Capture the computer's current Unix time.
        computer_epoch = time.time()

        # Display the computer's UTC time.
        computer_utc = datetime.now(timezone.utc)

        print("Computer UTC:", computer_utc)
        print("\nMT5 TICK COMPARISONS")
        print("-" * 65)

        # Store timestamp differences for comparison.
        differences = []

        # Check each currency pair individually.
        for symbol in WATCHLIST:

            # Retrieve the latest available market tick.
            tick = mt5.symbol_info_tick(symbol)

            if tick is None:

                print(symbol, "- No tick available")
                continue

            # Compare the raw MT5 timestamp with computer time.
            difference = tick.time_msc / 1000 - computer_epoch

            # Store the result.
            differences.append(difference)

            # Convert the tick timestamp for display.
            tick_utc = datetime.fromtimestamp(
                tick.time,
                tz=timezone.utc
            )

            print(
                f"{symbol}: "
                f"Tick={tick_utc.strftime('%Y-%m-%d %H:%M:%S')} | "
                f"Difference={difference:.2f} seconds"
            )

        # Summarise the results.
        print("\nSUMMARY")
        print("-" * 65)

        if differences:

            average_difference = sum(differences) / len(differences)

            print("Pairs checked:", len(differences))
            print(
                "Average timestamp difference:",
                round(average_difference, 2),
                "seconds"
            )
            print(
                "Average difference in hours:",
                round(average_difference / 3600, 4)
            )

        else:

            print("No usable market ticks were retrieved.")

    finally:

        # Close the MT5 connection.
        mt5.shutdown()

print("\n=== MULTI-SYMBOL CLOCK TEST FINISHED ===")
