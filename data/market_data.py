
# ==========================================
# FOREXAI: MARKET DATA ENGINE
# ==========================================

# Handles:
# - Broker UTC offset detection
# - Historical Forex market data retrieval
# - Timestamp conversion
# - Multi-symbol and multi-timeframe collection


import time

import MetaTrader5 as mt5
import pandas as pd

from datetime import datetime, timezone

from config.market_settings import BROKER_UTC_OFFSET_SECONDS


# ==========================================
# BROKER OFFSET DETECTION SETTINGS
# ==========================================

# Maximum acceptable age of a corrected market tick.
MAX_TICK_AGE_SECONDS = 300

# Allow a small future difference caused by timing.
MAX_FUTURE_TICK_SECONDS = 10

# Broker timezone offsets are estimated using
# 15-minute increments to support fractional timezones.
OFFSET_INCREMENT_SECONDS = 900

# Plausible timezone offset boundaries.
MIN_BROKER_OFFSET_SECONDS = -12 * 3600
MAX_BROKER_OFFSET_SECONDS = 14 * 3600


# ==========================================
# AUTOMATIC BROKER UTC OFFSET DETECTION
# ==========================================

def detect_broker_utc_offset():
    """
    Estimate the broker's current UTC offset using
    a live EURUSD tick and the computer's UTC clock.

    IMPORTANT:
    MT5 must already be initialised before calling
    this function.

    Returns:
        int: Detected broker UTC offset in seconds.

        None: If detection fails or the tick is unreliable.

    This function does not modify the central configuration.
    """

    # Ensure EURUSD is available in Market Watch.
    if not mt5.symbol_select("EURUSD", True):
        print(
            "WARNING: Could not select EURUSD for "
            "broker offset detection."
        )
        return None

    # Retrieve the latest available EURUSD tick.
    tick = mt5.symbol_info_tick("EURUSD")

    if tick is None:
        print(
            "WARNING: No EURUSD tick available for "
            "broker offset detection."
        )
        return None

    # Use millisecond precision when available.
    if tick.time_msc:
        raw_tick_epoch = tick.time_msc / 1000
    else:
        raw_tick_epoch = float(tick.time)

    # Capture computer UTC immediately after retrieving
    # the tick to reduce measurement timing differences.
    computer_epoch = time.time()

    # Estimate the difference between broker time
    # and the computer's UTC clock.
    estimated_offset = raw_tick_epoch - computer_epoch

    # Round to the nearest 15-minute timezone increment.
    detected_offset = round(
        estimated_offset / OFFSET_INCREMENT_SECONDS
    ) * OFFSET_INCREMENT_SECONDS

    # Reject implausible timezone offsets.
    if not (
        MIN_BROKER_OFFSET_SECONDS
        <= detected_offset
        <= MAX_BROKER_OFFSET_SECONDS
    ):
        print(
            "WARNING: Detected broker offset is outside "
            "the supported timezone range."
        )
        return None

    # Convert the tick timestamp into UTC using
    # the estimated broker offset.
    corrected_tick_epoch = (
        raw_tick_epoch - detected_offset
    )

    # Calculate the age of the corrected tick.
    tick_age = computer_epoch - corrected_tick_epoch

    # Reject ticks that are too old.
    if tick_age > MAX_TICK_AGE_SECONDS:
        print(
            f"WARNING: EURUSD tick is stale "
            f"({tick_age:.2f} seconds old)."
        )
        return None

    # Reject timestamps that are too far into the future.
    if tick_age < -MAX_FUTURE_TICK_SECONDS:
        print(
            f"WARNING: Corrected EURUSD tick is "
            f"{abs(tick_age):.2f} seconds in the future."
        )
        return None

    # Display successful detection information.
    print("\nBROKER UTC OFFSET DETECTED")
    print("--------------------------------")
    print(f"Estimated offset: {estimated_offset:.3f} seconds")
    print(f"Detected offset: {detected_offset} seconds")
    print(f"Detected timezone: UTC{detected_offset / 3600:+.2f}")
    print(f"Corrected tick age: {tick_age:.3f} seconds")

    return detected_offset


# ==========================================
# CENTRAL TIMESTAMP CONVERSION
# ==========================================

def convert_broker_timestamps_to_utc(
    timestamps,
    broker_utc_offset_seconds=None
):
    """
    Convert broker timestamps into UTC-aware Pandas
    datetime values.

    Accepts Python lists and Pandas Series.
    """

    # Use the supplied offset or fall back to the
    # centrally configured broker offset.
    active_offset = (
        broker_utc_offset_seconds
        if broker_utc_offset_seconds is not None
        else BROKER_UTC_OFFSET_SECONDS
    )

    # Convert the input into a Pandas Series.
    # This allows us to handle both lists and Series.
    timestamp_series = pd.Series(timestamps)

    # Remove the broker's UTC offset.
    corrected_timestamps = (
        timestamp_series - active_offset
    )

    # Convert Unix timestamps into UTC-aware datetimes.
    return pd.to_datetime(
        corrected_timestamps,
        unit="s",
        utc=True
    )

# ==========================================
# SINGLE-SYMBOL HISTORICAL DATA
# ==========================================

def get_historical_data(
    symbol,
    timeframe,
    number_of_candles=100
):
    """
    Retrieve historical candlestick data from MT5.

    The broker offset is detected once after connecting.
    If detection fails, the configured offset is used.
    """

    print(f"\nRetrieving market data for {symbol}...")

    # Initialise the MT5 connection.
    if not mt5.initialize():
        print("MT5 connection failed:", mt5.last_error())
        return None

    try:

        # Detect the current broker UTC offset.
        detected_offset = detect_broker_utc_offset()

        # Use the detected offset when available.
        # Otherwise, use the configured fallback.
        if detected_offset is not None:
            active_offset = detected_offset
            print("Using automatically detected broker offset.")
        else:
            active_offset = BROKER_UTC_OFFSET_SECONDS
            print("Using configured broker offset as fallback.")

        # Check whether the requested currency pair exists.
        symbol_info = mt5.symbol_info(symbol)

        if symbol_info is None:
            print(f"Currency pair not found: {symbol}")
            return None

        # Make the currency pair available in Market Watch.
        if not mt5.symbol_select(symbol, True):
            print(f"Could not select {symbol}")
            return None

        # Retrieve completed historical candles.
        # Position 1 excludes the currently forming candle.
        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            1,
            number_of_candles
        )

        if rates is None or len(rates) == 0:
            print("No historical data received.")
            print("MT5 error:", mt5.last_error())
            return None

        # Convert retrieved rates into a DataFrame.
        df = pd.DataFrame(rates)

        # Apply the selected broker offset.
        df["time"] = convert_broker_timestamps_to_utc(
            df["time"],
            active_offset
        )

        print(
            f"Successfully retrieved {len(df)} "
            f"candles for {symbol}."
        )

        return df

    finally:

        # Close the MT5 connection.
        mt5.shutdown()


# ==========================================
# MULTI-SYMBOL, MULTI-TIMEFRAME DATA
# ==========================================

def get_watchlist_market_data(number_of_candles=100):
    """
    Retrieve historical market data for all ForexAI
    watchlist pairs across multiple timeframes.

    One MT5 connection is used for the entire collection.

    One broker offset is detected and shared across
    every currency pair and timeframe in that collection.
    """

    # Initial ForexAI currency pair watchlist.
    watchlist = [
        "EURUSD",
        "USDJPY",
        "GBPUSD",
        "EURJPY",
        "GBPJPY",
        "AUDUSD",
        "USDCAD",
        "USDCHF"
    ]

    # Supported market-data timeframes.
    timeframes = {
        "M15": mt5.TIMEFRAME_M15,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4
    }

    # Stores all retrieved market data.
    market_data = {}

    print("\n=== FOREXAI: MULTI-TIMEFRAME DATA COLLECTION ===")

    # Establish one MT5 connection.
    if not mt5.initialize():
        print("MT5 connection failed:", mt5.last_error())
        return None

    try:

        # Detect the broker offset once for this collection.
        detected_offset = detect_broker_utc_offset()

        # Select the offset used by every dataset.
        if detected_offset is not None:
            active_offset = detected_offset
            print("\nUsing automatically detected broker offset.")
        else:
            active_offset = BROKER_UTC_OFFSET_SECONDS
            print("\nUsing configured broker offset as fallback.")

        print(
            "Active broker UTC offset:",
            active_offset,
            "seconds"
        )

        # Process every currency pair.
        for symbol in watchlist:

            print(f"\nCollecting data for {symbol}...")

            # Create a separate section for this pair.
            market_data[symbol] = {}

            # Confirm that the symbol exists.
            symbol_info = mt5.symbol_info(symbol)

            if symbol_info is None:
                print(f"Symbol unavailable: {symbol}")
                market_data[symbol] = None
                continue

            # Make the symbol available in Market Watch.
            if not mt5.symbol_select(symbol, True):
                print(f"Could not select symbol: {symbol}")
                market_data[symbol] = None
                continue

            # Retrieve every supported timeframe.
            for timeframe_name, timeframe_value in timeframes.items():

                print(f"  Retrieving {timeframe_name} data...")

                # Position 1 excludes the current forming candle.
                rates = mt5.copy_rates_from_pos(
                    symbol,
                    timeframe_value,
                    1,
                    number_of_candles
                )

                # Handle unavailable historical data.
                if rates is None or len(rates) == 0:

                    print(
                        f"  No {timeframe_name} data available "
                        f"for {symbol}."
                    )

                    market_data[symbol][timeframe_name] = None
                    continue

                # Convert MT5 rates into a DataFrame.
                df = pd.DataFrame(rates)

                # Apply the same selected broker offset
                # to every pair and timeframe.
                df["time"] = convert_broker_timestamps_to_utc(
                    df["time"],
                    active_offset
                )

                # Store the completed dataset.
                market_data[symbol][timeframe_name] = df

                print(
                    f"  Retrieved {len(df)} "
                    f"{timeframe_name} candles."
                )

        print("\nMulti-timeframe collection finished.")

        return market_data

    finally:

        # Close the MT5 connection after collection.
        mt5.shutdown()
