# ==========================================
# FOREXAI: TECHNICAL INDICATOR PIPELINE
# ==========================================

# Connects the technical indicator calculations
# to ForexAI's multi-pair, multi-timeframe market data.


import pandas as pd

from analysis.technical_indicators import (
    calculate_ema,
    calculate_rsi,
    calculate_atr
)


# ==========================================
# INDICATOR SETTINGS
# ==========================================

# Moving average periods used for trend analysis.
EMA_FAST_PERIOD = 20
EMA_SLOW_PERIOD = 50

# Momentum indicator period.
RSI_PERIOD = 14

# Volatility indicator period.
ATR_PERIOD = 14



# ==========================================
# PROCESS ONE TIMEFRAME
# ==========================================

def add_technical_indicators(data):
    """
    Calculate and attach technical indicators to one
    symbol/timeframe DataFrame.

    The original DataFrame is not modified.
    """

    # Handle a missing dataset.
    if data is None:
        return None

    # Confirm that the supplied data is a Pandas DataFrame.
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Market data must be a Pandas DataFrame.")

    # Confirm that the required MT5 price columns exist.
    required_columns = ["high", "low", "close"]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Market data is missing required columns: {missing_columns}"
        )

    # We need at least 50 candles to calculate EMA 50.
    minimum_candles = max(
        EMA_SLOW_PERIOD,
        RSI_PERIOD + 1,
        ATR_PERIOD
    )

    if len(data) < minimum_candles:
        raise ValueError(
            f"At least {minimum_candles} candles are required. "
            f"Received {len(data)}."
        )

    # Work on a copy to protect the original market data.
    enriched_data = data.copy()

    # ------------------------------------------
    # 1. EXPONENTIAL MOVING AVERAGES
    # ------------------------------------------

    # EMA 20: shorter-term trend.
    enriched_data["ema_20"] = calculate_ema(
        enriched_data["close"],
        EMA_FAST_PERIOD
    )

    # EMA 50: longer-term trend.
    enriched_data["ema_50"] = calculate_ema(
        enriched_data["close"],
        EMA_SLOW_PERIOD
    )

    # ------------------------------------------
    # 2. RELATIVE STRENGTH INDEX
    # ------------------------------------------

    # RSI 14: measures price momentum.
    enriched_data["rsi_14"] = calculate_rsi(
        enriched_data["close"],
        RSI_PERIOD
    )

    # ------------------------------------------
    # 3. AVERAGE TRUE RANGE
    # ------------------------------------------

    # The ATR function expects capitalized OHLC
    # column names. Rename a temporary copy so
    # the original MT5 column names stay unchanged.
    atr_data = enriched_data.rename(
        columns={
            "high": "High",
            "low": "Low",
            "close": "Close"
        }
    )[["High", "Low", "Close"]]

    # ATR 14: measures market volatility.
    enriched_data["atr_14"] = calculate_atr(
        atr_data,
        ATR_PERIOD
    )

    # Return the original candle data with
    # the four additional indicator columns.
    return enriched_data



# ==========================================
# PROCESS ALL MARKET DATA
# ==========================================

def process_market_data(market_data):
    """
    Process all available currency pairs and timeframes.

    Each available DataFrame receives:
    - EMA 20
    - EMA 50
    - RSI 14
    - ATR 14

    Missing symbol or timeframe datasets are preserved
    as None rather than causing the entire process to fail.
    """

    # Confirm that the input has the expected dictionary structure.
    if not isinstance(market_data, dict):
        raise TypeError("Market data must be a dictionary.")

    # Create a new dictionary to hold the enriched datasets.
    enriched_market_data = {}

    # Loop through each currency pair.
    for symbol, timeframe_data in market_data.items():

        # Preserve unavailable currency-pair data.
        if timeframe_data is None:
            enriched_market_data[symbol] = None
            continue

        # Each available currency pair should contain
        # a dictionary of its timeframe datasets.
        if not isinstance(timeframe_data, dict):
            raise TypeError(
                f"Invalid timeframe data for {symbol}. "
                "Expected a dictionary."
            )

        # Prepare a dictionary for this currency pair.
        enriched_market_data[symbol] = {}

        # Loop through M15, H1, and H4 datasets.
        for timeframe, dataframe in timeframe_data.items():

            # Preserve unavailable timeframe data.
            if dataframe is None:
                enriched_market_data[symbol][timeframe] = None
                continue

            try:
                # Calculate and attach the indicators.
                enriched_market_data[symbol][timeframe] = (
                    add_technical_indicators(dataframe)
                )

            except (TypeError, ValueError) as error:
                # Identify exactly which dataset caused the problem.
                raise ValueError(
                    f"Failed to process {symbol} {timeframe}: {error}"
                ) from error

    # Return all currency pairs with their enriched datasets.
    return enriched_market_data
