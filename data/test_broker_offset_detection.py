
# ==========================================
# FOREXAI: BROKER UTC OFFSET DETECTION TEST
# ==========================================

import time
import MetaTrader5 as mt5

from datetime import datetime, timezone

from config.market_settings import BROKER_UTC_OFFSET_SECONDS


# Maximum acceptable age of the corrected tick.
MAX_TICK_AGE_SECONDS = 300

# Allow a small future difference caused by timing.
MAX_FUTURE_TICK_SECONDS = 10


print("\n=== FOREXAI: BROKER OFFSET DETECTION TEST ===\n")

try:

    # Connect to the running MetaTrader 5 terminal.
    if not mt5.initialize():
        raise RuntimeError(
            f"MT5 connection failed: {mt5.last_error()}"
        )

    # Make EURUSD available for price updates.
    if not mt5.symbol_select("EURUSD", True):
        raise RuntimeError(
            f"Could not select EURUSD: {mt5.last_error()}"
        )

    # Retrieve the latest available EURUSD tick.
    tick = mt5.symbol_info_tick("EURUSD")

    if tick is None:
        raise RuntimeError(
            f"Could not retrieve EURUSD tick: {mt5.last_error()}"
        )

    # Use the millisecond timestamp when available.
    if tick.time_msc:
        raw_tick_epoch = tick.time_msc / 1000
    else:
        raw_tick_epoch = float(tick.time)

    # Capture computer UTC immediately after retrieving
    # the tick to minimise measurement timing differences.
    computer_epoch = time.time()

    # Estimate the broker's UTC offset.
    estimated_offset = raw_tick_epoch - computer_epoch

    # Determine the nearest whole-hour broker offset.
    detected_offset = round(
        estimated_offset / 3600
    ) * 3600

    # Correct the broker timestamp into UTC.
    corrected_tick_epoch = (
        raw_tick_epoch - detected_offset
    )

    # Calculate how old the corrected tick is.
    tick_age = computer_epoch - corrected_tick_epoch

    # ==========================================
    # VALIDATION
    # ==========================================

    # Reject ticks that are too old.
    if tick_age > MAX_TICK_AGE_SECONDS:
        raise RuntimeError(
            f"Tick is stale: {tick_age:.2f} seconds old. "
            "Automatic offset detection rejected."
        )

    # Reject timestamps too far into the future.
    if tick_age < -MAX_FUTURE_TICK_SECONDS:
        raise RuntimeError(
            f"Tick is unexpectedly in the future: "
            f"{tick_age:.2f} seconds."
        )

    # ==========================================
    # RESULTS
    # ==========================================

    corrected_tick_utc = datetime.fromtimestamp(
        corrected_tick_epoch,
        tz=timezone.utc
    )

    computer_datetime = datetime.fromtimestamp(
        computer_epoch,
        tz=timezone.utc
    )

    print("COMPUTER UTC")
    print("--------------------------------")
    print(computer_datetime)

    print("\nBROKER OFFSET DETECTION")
    print("--------------------------------")
    print(f"Estimated offset: {estimated_offset:.3f} seconds")
    print(f"Detected offset: {detected_offset} seconds")
    print(f"Detected offset: {detected_offset / 3600:+.1f} hours")

    print("\nCORRECTED MARKET TICK")
    print("--------------------------------")
    print("Original tick timestamp:", raw_tick_epoch)
    print("Corrected tick UTC:", corrected_tick_utc)

    print("\nTICK VALIDATION")
    print("--------------------------------")
    print(f"Corrected tick age: {tick_age:.3f} seconds")

    print("\nCONFIGURATION COMPARISON")
    print("--------------------------------")
    print(
        "Currently configured offset:",
        BROKER_UTC_OFFSET_SECONDS,
        "seconds"
    )

    if detected_offset == BROKER_UTC_OFFSET_SECONDS:
        print("Configuration status: MATCH")
    else:
        print("Configuration status: OFFSET CHANGE DETECTED")

    print("\n=== BROKER OFFSET DETECTION PASSED ===")

finally:

    # Close the Python connection to MT5.
    mt5.shutdown()

