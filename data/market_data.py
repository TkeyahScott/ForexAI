import MetaTrader5 as mt5
import pandas as pd


def get_historical_data(symbol, timeframe, number_of_candles=100):
    """
    Retrieve historical candlestick data from MetaTrader 5.
    """

    print(f"\nRetrieving market data for {symbol}...")

    # Check whether MT5 can be initialised.
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

        # Retrieve historical candlestick data.
        # Start at position 1 to exclude the currently forming candle.
        # This ensures we retrieve completed candles for technical analysis.
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

        # Convert the retrieved data into a DataFrame.
        df = pd.DataFrame(rates)

        # Convert timestamps into UTC-aware datetime values.
        df["time"] = pd.to_datetime(
            df["time"],
            unit="s",
            utc=True
        )

        print(f"Successfully retrieved {len(df)} candles for {symbol}.")

        return df

    finally:
        mt5.shutdown()
