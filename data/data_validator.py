
# ==========================================
# FOREXAI: MARKET DATA VALIDATOR
# ==========================================

# Pandas is used to inspect and validate
# the market data collected from MetaTrader 5.
import pandas as pd


# ==========================================
# STEP 1: CHECK FOR EMPTY OR MISSING DATA
# ==========================================

# ==========================================
# STEP 1: COMPLETE MARKET DATA VALIDATION
# ==========================================

def validate_market_data(data):
    """
    Perform all market-data validation checks.

    This function acts as the central validation
    coordinator by calling the individual checks
    for missing data, duplicate candles,
    chronological order and OHLC integrity.

    Returns:
        A dictionary containing the overall
        validation result and all detected errors.
    """

    # Confirm that the supplied information is
    # actually a Pandas DataFrame.
    if not isinstance(data, pd.DataFrame):
        return {
            "valid": False,
            "errors": [
                "Market data must be a Pandas DataFrame."
            ]
        }

    # Reject empty datasets immediately.
    if data.empty:
        return {
            "valid": False,
            "errors": [
                "Market data is empty."
            ]
        }

    # Store all validation errors in one list.
    errors = []

    # Check 1: Missing values.
    missing_values = data.isnull().sum()

    # These columns have dedicated validation functions.
    # Their missing values are handled separately.
    specialized_columns = {
        "time",
        "open",
        "high",
        "low",
        "close"
    }

    for column, count in missing_values.items():

        if count > 0 and column not in specialized_columns:

            errors.append(
                f"{column} contains {count} missing value(s)."
            )
        
    # Check 2 and 3: Timestamp validation.
    # Check whether the timestamp column exists before
    # running the individual timestamp validation checks.

    if "time" not in data.columns:

        errors.append(
            "Market data does not contain a time column."
        )

    else:

        # Check 2: Duplicate candle timestamps.
        duplicate_result = validate_duplicate_candles(data)
        errors.extend(duplicate_result["errors"])

        # Check 3: Chronological candle order.
        order_result = validate_candle_order(data)
        errors.extend(order_result["errors"])


    # Check 4: OHLC price integrity.
    ohlc_result = validate_ohlc_prices(data)
    errors.extend(ohlc_result["errors"])

    # Return one combined validation result.
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
    
    
    
    
# ==========================================
# STEP 2: CHECK FOR DUPLICATE CANDLES
# ==========================================

def validate_duplicate_candles(data):
    """
    Check whether market data contains duplicate
    candle timestamps.

    Each candle should have a unique timestamp
    within its currency pair and timeframe.

    Returns:
        A dictionary containing the validation
        result and any detected problems.
    """

    # Check that the supplied information is a DataFrame.
    if not isinstance(data, pd.DataFrame):
        return {
            "valid": False,
            "errors": ["Market data must be a Pandas DataFrame."]
        }

    # Check that the dataset is not empty.
    if data.empty:
        return {
            "valid": False,
            "errors": ["Market data is empty."]
        }

    # Confirm that a timestamp column exists.
    if "time" not in data.columns:
        return {
            "valid": False,
            "errors": ["Market data does not contain a time column."]
        }

    # Identify timestamps that appear more than once.
    duplicate_mask = data.duplicated(subset=["time"], keep=False)

    # Count all rows involved in duplicate timestamps.
    duplicate_count = int(duplicate_mask.sum())

    # Return an error if duplicate candles are found.
    if duplicate_count > 0:
        return {
            "valid": False,
            "errors": [
                f"Found {duplicate_count} rows with duplicate candle timestamps."
            ]
        }

    # No duplicate timestamps were detected.
    return {
        "valid": True,
        "errors": []
    }



# ==========================================
# STEP 3: CHECK CHRONOLOGICAL CANDLE ORDER
# ==========================================

def validate_candle_order(data):
    """
    Check whether market candles are arranged
    chronologically from oldest to newest.

    Returns:
        A dictionary containing the validation
        result and any detected problems.
    """

    # Confirm that the supplied data is a DataFrame.
    if not isinstance(data, pd.DataFrame):
        return {
            "valid": False,
            "errors": ["Market data must be a Pandas DataFrame."]
        }

    # Make sure the dataset contains records.
    if data.empty:
        return {
            "valid": False,
            "errors": ["Market data is empty."]
        }

    # Confirm that a timestamp column exists.
    if "time" not in data.columns:
        return {
            "valid": False,
            "errors": ["Market data does not contain a time column."]
        }

    # Check that timestamps are not missing.
    if data["time"].isnull().any():
        return {
            "valid": False,
            "errors": ["Candle timestamps contain missing values."]
        }

    # Check whether timestamps are in ascending order.
    if not data["time"].is_monotonic_increasing:
        return {
            "valid": False,
            "errors": [
                "Candle timestamps are not in chronological order."
            ]
        }

    # The candle sequence is correctly ordered.
    return {
        "valid": True,
        "errors": []
    }



# ==========================================
# STEP 4: CHECK OHLC PRICE INTEGRITY
# ==========================================

def validate_ohlc_prices(data):
    """
    Check whether Open, High, Low and Close prices
    follow the correct OHLC relationships.

    This helps detect inconsistent or corrupted
    market candle data.

    Returns:
        A dictionary containing the validation
        result and any detected problems.
    """

    # Confirm that the supplied data is a DataFrame.
    if not isinstance(data, pd.DataFrame):
        return {
            "valid": False,
            "errors": ["Market data must be a Pandas DataFrame."]
        }

    # Make sure the dataset contains records.
    if data.empty:
        return {
            "valid": False,
            "errors": ["Market data is empty."]
        }

    # Identify the four required OHLC columns.
    required_columns = ["open", "high", "low", "close"]

    # Find any OHLC columns that are missing.
    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        return {
            "valid": False,
            "errors": [
                f"Missing required OHLC column(s): {', '.join(missing_columns)}."
            ]
        }

    errors = []

    # Check each OHLC column for missing values
    # and values that cannot be interpreted as numbers.
    for column in required_columns:

        if data[column].isnull().any():
            errors.append(
                f"{column} contains missing price values."
            )

        # Convert a temporary copy to numeric values.
        # The original market data is not modified.
        numeric_values = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        # Detect non-numeric values separately.
        invalid_values = (
            numeric_values.isnull()
            & data[column].notnull()
        )

        if invalid_values.any():
            errors.append(
                f"{column} contains non-numeric price values."
            )

    # Stop relationship checks if prices are missing
    # or cannot be converted into numbers.
    if errors:
         return {
            "valid": False,
            "errors": errors
        }

    # Create temporary numeric versions of the OHLC columns.
    prices = data[required_columns].apply(
        pd.to_numeric,
        errors="coerce"
    )

    # Check for infinite price values.
    # Infinite values cannot represent valid Forex prices.
    infinite_prices = prices.isin([float("inf"), float("-inf")])

    if infinite_prices.any().any():
       errors.append(
          "OHLC prices contain infinite values."
    )

    # Stop validation if any infinite prices are detected.
# Invalid values must not proceed into OHLC calculations.
    if errors:
       return {
        "valid": False,
        "errors": errors
    }

    # Check that all OHLC prices are greater than zero.
    # Forex currency prices should never be zero or negative.
    non_positive_prices = prices[required_columns] <= 0

    if non_positive_prices.any().any():
        errors.append(
            "OHLC prices contain zero or negative values."
        )

    # Stop validation if any prices are zero or negative.
    # Invalid prices must not proceed into OHLC relationship checks.
    if errors:
       return {
           "valid": False,
           "errors": errors
        }
    # Check that High is not below Open or Close.
    invalid_high = (
        (prices["high"] < prices["open"])
        | (prices["high"] < prices["close"])
    )

    if invalid_high.any():
        errors.append(
            "High price is lower than Open or Close."
        )

    # Check that Low is not above Open or Close.
    invalid_low = (
        (prices["low"] > prices["open"])
        | (prices["low"] > prices["close"])
    )

    if invalid_low.any():
        errors.append(
            "Low price is higher than Open or Close."
        )

    # Check that High is not below Low.
    if (prices["high"] < prices["low"]).any():
        errors.append(
            "High price is lower than Low price."
        )

    # Return the final validation result.
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


