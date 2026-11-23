
# Import tools for reading and comparing timestamps.
from datetime import datetime, timezone
import time

# Import the MetaTrader 5 Python package.
import MetaTrader5 as mt5


# ==========================================
# FOREXAI: TIMESTAMP DIAGNOSTICS
# ==========================================

print("\n=== FOREXAI: TIMESTAMP DIAGNOSTICS ===\n")

# Connect to the currently running MT5 terminal.
if not mt5.initialize():

    print("MT5 connection failed:", mt5.last_error())

else:

    try:
        # Record the computer's current Unix timestamp.
        # Unix timestamps represent seconds since 1 January 1970.
        computer_epoch = time.time()

        # Record the computer's current UTC datetime.
        computer_utc = datetime.now(timezone.utc)

        print("COMPUTER CLOCK")
        print("------------------------------------------")
        print("Computer Unix timestamp:", computer_epoch)
        print("Computer UTC time:", computer_utc)

        # Retrieve the latest EURUSD market tick.
        tick = mt5.symbol_info_tick("EURUSD")

        if tick is None:

            print("\nCould not retrieve EURUSD tick.")
            print("MT5 error:", mt5.last_error())

        else:

            # Read the raw timestamp supplied by MT5.
            tick_epoch = tick.time

            # Convert the MT5 timestamp into a UTC datetime.
            tick_utc = datetime.fromtimestamp(
                tick_epoch,
                tz=timezone.utc
            )

            print("\nMT5 LIVE TICK")
            print("------------------------------------------")
            print("Raw tick timestamp:", tick_epoch)
            print("Tick UTC conversion:", tick_utc)

            # Compare the MT5 timestamp with the computer timestamp.
            tick_difference = tick_epoch - computer_epoch

            print(
                "Tick minus computer time:",
                round(tick_difference, 2),
                "seconds"
            )

            # Print the millisecond timestamp when available.
            print("Raw tick milliseconds:", tick.time_msc)

        # Retrieve three completed EURUSD H1 candles.
        rates = mt5.copy_rates_from_pos(
            "EURUSD",
            mt5.TIMEFRAME_H1,
            1,
            3
        )

        if rates is None or len(rates) == 0:

            print("\nCould not retrieve historical candles.")

        else:

            print("\nMT5 HISTORICAL CANDLES")
            print("------------------------------------------")

            # Display the raw timestamp and UTC conversion
            # for each of the three completed candles.
            for candle in rates:

                candle_epoch = int(candle["time"])

                candle_utc = datetime.fromtimestamp(
                    candle_epoch,
                    tz=timezone.utc
                )

                print(
                    "Raw:",
                    candle_epoch,
                    "| UTC conversion:",
                    candle_utc
                )

    finally:

        # Close the MT5 connection after testing.
        mt5.shutdown()

print("\n=== DIAGNOSTICS FINISHED ===")
