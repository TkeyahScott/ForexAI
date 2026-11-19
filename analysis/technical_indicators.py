
import pandas as pd
import numpy as np

# ==========================================
# FOREXAI: TECHNICAL INDICATORS
# ==========================================

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
