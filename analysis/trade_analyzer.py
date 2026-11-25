
# ==========================================
# FOREXAI: TRADE ANALYZER
# ==========================================

# Handles multi-timeframe market analysis.
# The analyzer uses market data that has already
# been processed by the indicator pipeline.

import math

# ==========================================
# H4 MAIN TREND ANALYSIS
# ==========================================

def analyze_h4_trend(h4_data):
    """
    Identify the main market trend using H4 data.

    Bullish:
        EMA20 > EMA50
        Latest close > EMA20

    Bearish:
        EMA20 < EMA50
        Latest close < EMA20

    Neutral:
        Conditions are conflicting or incomplete.

    Returns:
        str: BULLISH, BEARISH or NEUTRAL
    """

    # Ensure H4 market data is available.
    if h4_data is None or h4_data.empty:
        return "NEUTRAL"

    # Required columns for H4 trend analysis.
    required_columns = [
        "close",
        "ema_20",
        "ema_50"
    ]

    # Check that all required columns exist.
    if not all(
        column in h4_data.columns
        for column in required_columns
    ):
        return "NEUTRAL"

    # Retrieve the latest completed candle.
    latest_candle = h4_data.iloc[-1]

    # Extract the latest closing price and indicators.
    close_price = latest_candle["close"]
    ema_20 = latest_candle["ema_20"]
    ema_50 = latest_candle["ema_50"]

    # Ensure all required values are available.
    if any(
        value is None
        for value in [close_price, ema_20, ema_50]
    ):
        return "NEUTRAL"

    # Reject missing numerical values.
    if not all(
        __import__("math").isfinite(float(value))
        for value in [close_price, ema_20, ema_50]
    ):
        return "NEUTRAL"

    # Identify a bullish H4 trend.
    if ema_20 > ema_50 and close_price > ema_20:
        return "BULLISH"

    # Identify a bearish H4 trend.
    if ema_20 < ema_50 and close_price < ema_20:
        return "BEARISH"

    # Conditions do not establish a clear direction.
    return "NEUTRAL"



# ==========================================
# H1 TREND AND MOMENTUM CONFIRMATION
# ==========================================

def confirm_h1_trend(h1_data):
    """
    Confirm the market direction using H1 data.

    Bullish:
        EMA20 > EMA50
        RSI14 > 50

    Bearish:
        EMA20 < EMA50
        RSI14 < 50

    Neutral:
        Conditions conflict or data is incomplete.

    Returns:
        str: BULLISH, BEARISH or NEUTRAL
    """

    # Ensure H1 market data is available.
    if h1_data is None or h1_data.empty:
        return "NEUTRAL"

    # Required columns for H1 confirmation.
    required_columns = [
        "ema_20",
        "ema_50",
        "rsi_14"
    ]

    # Check that all required columns exist.
    if not all(
        column in h1_data.columns
        for column in required_columns
    ):
        return "NEUTRAL"

    # Retrieve the latest completed candle.
    latest_candle = h1_data.iloc[-1]

    # Extract the latest indicator values.
    ema_20 = latest_candle["ema_20"]
    ema_50 = latest_candle["ema_50"]
    rsi_14 = latest_candle["rsi_14"]

    # Ensure all values are valid numbers.
    try:
        ema_20 = float(ema_20)
        ema_50 = float(ema_50)
        rsi_14 = float(rsi_14)

    except (TypeError, ValueError):
        return "NEUTRAL"

    # Reject NaN and infinite values.
    if not all(
        math.isfinite(value)
        for value in [ema_20, ema_50, rsi_14]
    ):
        return "NEUTRAL"

    # RSI must be within its valid range.
    if not 0 <= rsi_14 <= 100:
        return "NEUTRAL"

    # Identify bullish H1 confirmation.
    if ema_20 > ema_50 and rsi_14 > 50:
        return "BULLISH"

    # Identify bearish H1 confirmation.
    if ema_20 < ema_50 and rsi_14 < 50:
        return "BEARISH"

    # Conditions are conflicting or neutral.
    return "NEUTRAL"


# ==========================================
# M15 ENTRY SIGNAL ANALYSIS
# ==========================================

def generate_m15_entry_signal(m15_data, h4_trend, h1_trend):
    """
    Identify a potential BUY or SELL entry using M15 data.

    BUY conditions:
        H4 trend is BULLISH.
        H1 confirmation is BULLISH.
        M15 candle touches or moves below EMA20.
        M15 candle closes above EMA20.
        M15 candle is bullish.
        RSI14 is above 50.

    SELL conditions:
        H4 trend is BEARISH.
        H1 confirmation is BEARISH.
        M15 candle touches or moves above EMA20.
        M15 candle closes below EMA20.
        M15 candle is bearish.
        RSI14 is below 50.

    Returns:
        str: BUY, SELL or NO TRADE
    """

    # Higher timeframes must agree before considering an entry.
    if h4_trend != h1_trend:
        return "NO TRADE"

    # Only bullish or bearish conditions are eligible.
    if h4_trend not in ["BULLISH", "BEARISH"]:
        return "NO TRADE"

    # Ensure M15 market data is available.
    if m15_data is None or m15_data.empty:
        return "NO TRADE"

    # Required columns for M15 entry analysis.
    required_columns = [
        "open",
        "high",
        "low",
        "close",
        "ema_20",
        "rsi_14"
    ]

    # Check that all required columns exist.
    if not all(
        column in m15_data.columns
        for column in required_columns
    ):
        return "NO TRADE"

    # Retrieve the latest completed M15 candle.
    latest_candle = m15_data.iloc[-1]

    # Extract the required market values.
    try:
        open_price = float(latest_candle["open"])
        high_price = float(latest_candle["high"])
        low_price = float(latest_candle["low"])
        close_price = float(latest_candle["close"])
        ema_20 = float(latest_candle["ema_20"])
        rsi_14 = float(latest_candle["rsi_14"])

    except (TypeError, ValueError):
        return "NO TRADE"

    # Reject NaN and infinite values.
    if not all(
        math.isfinite(value)
        for value in [
            open_price,
            high_price,
            low_price,
            close_price,
            ema_20,
            rsi_14
        ]
    ):
        return "NO TRADE"

    # Validate the candle's price structure.
    if high_price < low_price:
        return "NO TRADE"

    if high_price < max(open_price, close_price):
        return "NO TRADE"

    if low_price > min(open_price, close_price):
        return "NO TRADE"

    # RSI must be within its valid range.
    if not 0 <= rsi_14 <= 100:
        return "NO TRADE"

    # --------------------------------------
    # BUY ENTRY CONDITIONS
    # --------------------------------------

    if h4_trend == "BULLISH":

        # Price must pull back to EMA20 and reclaim it.
        pullback_and_reclaim = (
            low_price <= ema_20
            and close_price > ema_20
        )

        # The completed candle must be bullish.
        bullish_candle = close_price > open_price

        # RSI must support bullish momentum.
        bullish_momentum = rsi_14 > 50

        if (
            pullback_and_reclaim
            and bullish_candle
            and bullish_momentum
        ):
            return "BUY"

    # --------------------------------------
    # SELL ENTRY CONDITIONS
    # --------------------------------------

    if h4_trend == "BEARISH":

        # Price must pull back to EMA20 and reject it.
        pullback_and_rejection = (
            high_price >= ema_20
            and close_price < ema_20
        )

        # The completed candle must be bearish.
        bearish_candle = close_price < open_price

        # RSI must support bearish momentum.
        bearish_momentum = rsi_14 < 50

        if (
            pullback_and_rejection
            and bearish_candle
            and bearish_momentum
        ):
            return "SELL"

    # No valid entry was identified.
    return "NO TRADE"