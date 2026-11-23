
# ==========================================
# FOREXAI: RAW MT5 CANDLE TIMESTAMP TEST
# ==========================================

import MetaTrader5 as mt5
from datetime import datetime, timezone

# Reference timestamp from our native MQL5 diagnostic.
NATIVE_CANDLE_EPOCH = 1794369600

print("\n=== FOREXAI: RAW CANDLE TIMESTAMP TEST ===\n")

try:
    # Connect to the currently running MT5 terminal.
    if not mt5.initialize():
        print("MT5 connection failed:", mt5.last_error())
        raise RuntimeError("Could not connect to MT5.")

    symbol = "EURUSD"
    timeframe = mt5.TIMEFRAME_H1

    # Request the latest completed H1 candles.
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 1, 3)

    if rates is None or len(rates) == 0:
        print("No historical candles received:", mt5.last_error())
        raise RuntimeError("Could not retrieve candle data.")

    # The final row contains the most recent completed candle.
    latest_candle = rates[-1]

    # Keep the original timestamp before any conversion.
    raw_epoch = int(latest_candle["time"])

    # Display the timestamp interpreted as UTC.
    python_utc = datetime.fromtimestamp(
        raw_epoch,
        tz=timezone.utc
    )

    print("PYTHON HISTORICAL CANDLE")
    print("--------------------------------")
    print("Raw candle timestamp:", raw_epoch)
    print("Python UTC conversion:", python_utc)

    print("\nNATIVE MT5 COMPARISON")
    print("--------------------------------")
    print("Native candle timestamp:", NATIVE_CANDLE_EPOCH)
    print("Difference in seconds:", raw_epoch - NATIVE_CANDLE_EPOCH)

    print("\n=== TEST FINISHED ===")

finally:
    # Close the Python connection without closing the MT5 terminal.
    mt5.shutdown()
