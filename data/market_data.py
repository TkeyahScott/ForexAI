
# ==========================================
# FOREXAI: MARKET DATA ENGINE
# ==========================================

# Handles:
# - Broker UTC offset detection
# - Historical Forex market data retrieval
# - Timestamp conversion
# - Multi-symbol and multi-timeframe collection


import MetaTrader5 as mt5
import pandas as pd


# ==========================================
# CENTRAL TIMESTAMP CONVERSION
# ==========================================

def convert_broker_timestamps_to_utc(timestamps):
    """
    Convert MT5 Unix timestamps into UTC-aware
    Pandas datetime values.

    MT5 Python API returns tick and bar timestamps
    in UTC. Therefore, no broker offset is subtracted.

    Accepts Python lists and Pandas Series.
    """

    # Convert the input into a Pandas Series.
    timestamp_series = pd.Series(timestamps)

    # Convert Unix timestamps directly into
    # UTC-aware datetime values.
    return pd.to_datetime(
        timestamp_series,
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

    MT5 Unix timestamps are converted directly into UTC.
    """

    print(f"\nRetrieving market data for {symbol}...")

    # Initialise the MT5 connection.
    if not mt5.initialize():
        print("MT5 connection failed:", mt5.last_error())
        return None

    try:

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

        # Convert MT5 candle timestamps directly into UTC.
        df["time"] = convert_broker_timestamps_to_utc(df["time"])

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

    All retrieved candle timestamps are converted
    directly into UTC.
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

                # Convert MT5 candle timestamps directly into UTC.
                df["time"] = convert_broker_timestamps_to_utc(df["time"])

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
