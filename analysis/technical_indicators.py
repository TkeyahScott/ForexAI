
import pandas as pd
import numpy as np

# ==========================================
# FOREXAI: TECHNICAL INDICATORS
# ==========================================

# ==========================================
# EXPONENTIAL MOVING AVERAGE (EMA)
# ==========================================


# ==========================================
# EMA CALCULATIONS
# (Exponential Moving Average): A technical indicator 
# that calculates the average price over a specified 
# period, giving greater weight to recent prices. 
# It helps identify market trends and potential changes
# in trend direction.
# ==========================================
# EMA helps it assess trend direction.


def calculate_ema(data, period):
    """
    Calculate the Exponential Moving Average (EMA).

    Args:
        data: Pandas Series containing closing prices.
        period: Number of candles used in the calculation.

    Returns:
        A Pandas Series containing the EMA values.
    """

    # Confirm that the supplied data is a Pandas Series.
    if not isinstance(data, pd.Series):
        raise TypeError(
            "EMA input must be a Pandas Series."
        )

    # Ensure that the requested period is a positive integer.
    if not isinstance(period, int) or isinstance(period, bool) or period <= 0:
        raise ValueError(
            "EMA period must be a positive integer."
        )

    # Reject empty price data.
    if data.empty:
        raise ValueError(
            "Cannot calculate EMA from empty data."
        )

    # Ensure all closing prices are numeric.
    prices = pd.to_numeric(data, errors="coerce")

    if prices.isnull().any():
        raise ValueError(
            "EMA input contains missing or non-numeric prices."
        )

    # Reject positive or negative infinite prices.
    if not np.isfinite(prices).all():
        raise ValueError(
            "EMA input contains infinite price values."
        )

    # Calculate the Exponential Moving Average.
    ema = prices.ewm(
        span=period,
        adjust=False,
        min_periods=period
    ).mean()

    return ema

# ------------------------------------------

# ==========================================
# RELATIVE STRENGTH INDEX (RSI)
# ==========================================


# ==========================================
# RSI CALCULATIONS
# (Relative Strength Index): A momentum indicator 
# that measures the speed and magnitude of recent 
# price movements on a scale of 0–100. It helps 
# identify potential overbought and oversold 
# market conditions.
# ==========================================
# RSI helps ForexAI assess momentum
# ==========================================


def calculate_rsi(data, period=14):
    """
    Calculate the Relative Strength Index (RSI).

    Args:
        data: Pandas Series containing closing prices.
        period: Number of candles used in the calculation.

    Returns:
        A Pandas Series containing RSI values.
    """
    
    # Confirm that the supplied data is a Pandas Series.
    if not isinstance(data, pd.Series):
        raise TypeError(
            "RSI input must be a Pandas Series."
        )

    # Ensure that the requested period is a positive integer.
    if not isinstance(period, int) or isinstance(period, bool) or period <= 0:
        raise ValueError(
            "RSI period must be a positive integer."
        )
        
    # Reject empty price data.
    if data.empty:
        raise ValueError(
            "Cannot calculate RSI from empty data."
        )

    # Ensure enough historical prices are available.
    if len(data) <= period:
        raise ValueError(
            "Not enough historical data to calculate RSI."
        )
        
    # Ensure all closing prices are numeric.
    prices = pd.to_numeric(data, errors="coerce")

    # Reject missing or non-numeric price values.
    if prices.isnull().any():
        raise ValueError(
            "RSI input contains missing or non-numeric prices."
        )
        
    # Reject positive or negative infinite prices.
    if not np.isfinite(prices).all():
        raise ValueError(
            "RSI input contains infinite price values."
        )
        
    # Calculate the change in closing price between candles.
    price_changes = prices.diff()

    # Separate upward and downward price movements.
    gains = price_changes.clip(lower=0)
    losses = -price_changes.clip(upper=0)
    
    # Calculate average gains using Wilder's smoothing method.
    average_gains = gains.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()

    # Calculate average losses using Wilder's smoothing method.
    average_losses = losses.ewm(
        alpha=1 / period,
        adjust=False,
        min_periods=period
    ).mean()
    
    # Calculate Relative Strength (RS).
    # RS compares average gains against average losses.
    relative_strength = average_gains / average_losses
    
    # Calculate RSI using Relative Strength.
    rsi = 100 - (100 / (1 + relative_strength))

    # Handle periods with gains but no losses.
    rsi = rsi.mask(
        (average_gains > 0) & (average_losses == 0),
        100
    )

    # Handle periods with losses but no gains.
    rsi = rsi.mask(
        (average_gains == 0) & (average_losses > 0),
        0
    )

    # Handle periods with no price movement.
    rsi = rsi.mask(
        (average_gains == 0) & (average_losses == 0),
        50
    )
    
    # Return the calculated RSI values.
    return rsi