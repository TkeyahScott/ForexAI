# Testing the timezones sent via market_data. 


# Import tools for checking UTC timestamps.
from datetime import datetime, timezone

# Import MetaTrader 5.
import MetaTrader5 as mt5


# ==========================================
# FOREXAI: MARKET CLOCK DIAGNOSTIC
# ==========================================

print("\n=== FOREXAI: MARKET CLOCK TEST ===\n")


# Connect to the running MT5 terminal.
if not mt5.initialize():

    print("MT5 connection failed:", mt5.last_error())

else:

    try:
        # Retrieve the latest available EURUSD market tick.
        tick = mt5.symbol_info_tick("EURUSD")

        if tick is None:

            print("Could not retrieve the EURUSD market tick.")
            print("MT5 error:", mt5.last_error())

        else:

            # Convert the MT5 tick timestamp into UTC.
            mt5_time = datetime.fromtimestamp(
                tick.time,
                tz=timezone.utc
            )

            # Get the computer's current UTC time.
            python_time = datetime.now(timezone.utc)

            # Calculate the difference between both timestamps.
            difference = (
                mt5_time - python_time
            ).total_seconds() / 60

            print("Computer UTC time:", python_time)
            print("Latest MT5 tick UTC:", mt5_time)

            print(
                "MT5 tick time difference:",
                round(difference, 2),
                "minutes"
            )

    finally:

        # Close the MT5 connection.
        mt5.shutdown()


print("\n=== CLOCK TEST FINISHED ===")
