
# ==========================================
# FOREXAI: RAW LIVE TICK TIMESTAMP TEST
# ==========================================

import MetaTrader5 as mt5
import time
from datetime import datetime, timezone

print("\n=== FOREXAI: RAW LIVE TICK TEST ===\n")

try:
    if not mt5.initialize():
        raise RuntimeError(f"MT5 connection failed: {mt5.last_error()}")

    # Capture the computer's UTC Unix timestamp.
    computer_epoch = time.time()

    # Retrieve the latest EURUSD market tick.
    tick = mt5.symbol_info_tick("EURUSD")

    if tick is None:
        raise RuntimeError(f"Could not retrieve tick: {mt5.last_error()}")

    # Preserve the original tick timestamp.
    raw_tick_epoch = tick.time

    # Convert the raw timestamp to UTC.
    tick_utc = datetime.fromtimestamp(
        raw_tick_epoch,
        tz=timezone.utc
    )

    computer_utc = datetime.fromtimestamp(
        computer_epoch,
        tz=timezone.utc
    )

    print("COMPUTER CLOCK")
    print("--------------------------------")
    print("Computer UTC:", computer_utc)
    print("Computer epoch:", computer_epoch)

    print("\nMT5 LIVE TICK")
    print("--------------------------------")
    print("Raw tick epoch:", raw_tick_epoch)
    print("Raw tick milliseconds:", tick.time_msc)
    print("Tick UTC conversion:", tick_utc)

    print("\nTIMESTAMP DIFFERENCE")
    print("--------------------------------")
    print("Tick minus computer (seconds):",
          raw_tick_epoch - computer_epoch)

    print("\n=== TEST FINISHED ===")

finally:
    mt5.shutdown()
