
# ==========================================
# FOREXAI: CORRECTED LIVE TICK TEST
# ==========================================

import MetaTrader5 as mt5
import time

from datetime import datetime, timezone

from data.market_data import (
    BROKER_UTC_OFFSET_SECONDS
)

print("\n=== FOREXAI: CORRECTED LIVE TICK TEST ===\n")

try:
    if not mt5.initialize():
        raise RuntimeError(f"MT5 connection failed: {mt5.last_error()}")

    # Capture the computer's current UTC time.
    computer_utc = time.time()

    # Retrieve the latest EURUSD tick.
    tick = mt5.symbol_info_tick("EURUSD")

    if tick is None:
        raise RuntimeError(f"Tick unavailable: {mt5.last_error()}")

    # Correct the broker's live tick timestamp.
    corrected_tick_epoch = (
        tick.time - BROKER_UTC_OFFSET_SECONDS
    )

    # Convert the corrected timestamp into UTC.
    corrected_tick_utc = datetime.fromtimestamp(
        corrected_tick_epoch,
        tz=timezone.utc
    )

    # Convert the computer timestamp into UTC.
    computer_datetime = datetime.fromtimestamp(
        computer_utc,
        tz=timezone.utc
    )

    print("COMPUTER UTC")
    print("--------------------------------")
    print(computer_datetime)

    print("\nCORRECTED EURUSD TICK")
    print("--------------------------------")
    print("Original broker timestamp:", tick.time)
    print("Corrected UTC timestamp:", corrected_tick_epoch)
    print("Corrected UTC datetime:", corrected_tick_utc)

    print("\nTIME DIFFERENCE")
    print("--------------------------------")
    print(
        "Tick minus computer (seconds):",
        corrected_tick_epoch - computer_utc
    )

    print("\n=== TEST FINISHED ===")

finally:
    mt5.shutdown()
