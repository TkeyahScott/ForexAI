import pandas as pd;
import numpy as np;


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
    Calculate the Relative Strength Index (RSI) using
    Wilder's standard smoothing method.

    Args:
        data: Pandas Series containing closing prices.
        period: Number of price changes used in the calculation.

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

    # Convert price values to numeric data.
    prices = pd.to_numeric(
        data.copy(),
        errors="coerce"
    )

    # Reject missing or non-numeric price values.
    if prices.isnull().any():
        raise ValueError(
            "RSI input contains missing or non-numeric price values."
        )

    # Reject positive or negative infinite prices.
    if not np.isfinite(prices.to_numpy()).all():
        raise ValueError(
            "RSI input contains infinite price values."
        )

    # Calculate the difference between consecutive closing prices.
    price_changes = prices.diff()

    # Separate upward and downward price movements.
    gains = price_changes.clip(lower=0)
    losses = -price_changes.clip(upper=0)

    # Create output Series for the smoothed averages.
    average_gains = pd.Series(
        np.nan,
        index=prices.index,
        dtype=float
    )

    average_losses = pd.Series(
        np.nan,
        index=prices.index,
        dtype=float
    )

    # Calculate the initial average gain and loss using
    # the simple average of the first 'period' price changes.
    average_gains.iloc[period] = gains.iloc[1:period + 1].mean()
    average_losses.iloc[period] = losses.iloc[1:period + 1].mean()

    # Apply Wilder's smoothing to all subsequent price changes.
    for i in range(period + 1, len(prices)):

        average_gains.iloc[i] = (
            (average_gains.iloc[i - 1] * (period - 1))
            + gains.iloc[i]
        ) / period

        average_losses.iloc[i] = (
            (average_losses.iloc[i - 1] * (period - 1))
            + losses.iloc[i]
        ) / period

    # Calculate the Relative Strength (RS).
    relative_strength = average_gains / average_losses

    # Calculate RSI from Relative Strength.
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

    # Handle periods with no gains and no losses.
    rsi = rsi.mask(
        (average_gains == 0) & (average_losses == 0),
        50
    )

    # Return the calculated RSI values.
    return rsi


# ==========================================
# AVERAGE TRUE RANGE (ATR)
# ==========================================


# ==========================================
# ATR CALCULATIONS
# (Average True Range): A volatility indicator
# that measures the average range of price
# movements over a specified period.
# It helps ForexAI assess market volatility.
# ==========================================

def calculate_atr(data, period=14):
    """
    Calculate the Average True Range (ATR).

    Args:
        data: Pandas DataFrame containing High, Low and Close prices.
        period: Number of candles used in the calculation.

    Returns:
        A Pandas Series containing ATR values.
    """

    # Confirm that the supplied data is a Pandas DataFrame.
    if not isinstance(data, pd.DataFrame):
        raise TypeError(
            "ATR input must be a Pandas DataFrame."
        )

    # Ensure that the requested period is a positive integer.
    if not isinstance(period, int) or isinstance(period, bool) or period <= 0:
        raise ValueError(
            "ATR period must be a positive integer."
        )

    # Reject empty market data.
    if data.empty:
        raise ValueError(
            "Cannot calculate ATR from empty data."
        )

    # Confirm that all required price columns are present.
    required_columns = ["High", "Low", "Close"]

    if not all(column in data.columns for column in required_columns):
        raise ValueError(
            "ATR input must contain High, Low and Close columns."
        )
        
    # Extract the required price columns.
    prices = data[required_columns].copy()

    # Ensure all price values are numeric.
    prices = prices.apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Reject missing or non-numeric price values.
    if prices.isnull().any().any():
        raise ValueError(
            "ATR input contains missing or non-numeric price values."
        )

    # Reject positive or negative infinite price values.
    if not np.isfinite(prices.to_numpy()).all():
        raise ValueError(
            "ATR input contains infinite price values."
        )

    # Ensure that High is not below Low.
    if (prices["High"] < prices["Low"]).any():
        raise ValueError(
            "ATR High prices cannot be lower than Low prices."
        )

    # Ensure that all prices are positive.
    if (prices <= 0).any().any():
        raise ValueError(
            "ATR input must contain positive price values."
        )
        
    # Ensure enough historical candles are available.
    if len(prices) < period:
        raise ValueError(
            "Not enough historical data to calculate ATR."
        )

    # Retrieve the previous candle's closing price.
    previous_close = prices["Close"].shift(1)

    # Calculate the three True Range components.
    high_low = prices["High"] - prices["Low"]

    high_previous_close = (
        prices["High"] - previous_close
    ).abs()

    low_previous_close = (
        prices["Low"] - previous_close
    ).abs()

    # Calculate True Range using the greatest of the three components.
    true_range = pd.concat(
        [
            high_low,
            high_previous_close,
            low_previous_close
        ],
        axis=1
    ).max(axis=1)
    
    # Ensure that Close falls within the candle's High-Low range.
    if (
        (prices["Close"] < prices["Low"]).any()
        or (prices["Close"] > prices["High"]).any()
    ):
        raise ValueError(
            "ATR Close prices must fall between High and Low."
        )
        
    # Create an ATR Series with the same index as the input data.
    atr = pd.Series(
        np.nan,
        index=prices.index,
        dtype=float
    )

    # Calculate the initial ATR using the average of the first
    # specified number of True Range values.
    atr.iloc[period - 1] = true_range.iloc[:period].mean()

    # Calculate subsequent ATR values using Wilder's smoothing.
    for i in range(period, len(true_range)):

        atr.iloc[i] = (
            (atr.iloc[i - 1] * (period - 1))
            + true_range.iloc[i]
        ) / period

    # Return the calculated ATR values.
    return atr