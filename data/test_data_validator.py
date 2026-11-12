
# ==========================================
# FOREXAI: DATA VALIDATOR TEST
# ==========================================

import MetaTrader5 as mt5

import pandas as pd

from data.data_validator import (
    validate_market_data,
    validate_duplicate_candles,
    validate_candle_order,
    validate_ohlc_prices
)

from data.market_data import get_historical_data

# Tests 1–10: Tests the following:
# DataFrame structure, missing data, 
# duplicate candles, and timestamp validation.

# ==========================================
# TEST 1: VALID MARKET DATA
# ==========================================

print("\nTEST 1: VALID MARKET DATA")

valid_data = pd.DataFrame({
    "time": [1794369600, 1794370500],
    "open": [1.1000, 1.1010],
    "high": [1.1050, 1.1060],
    "low": [1.0980, 1.0990],
    "close": [1.1030, 1.1040]
})

result = validate_market_data(valid_data)

print(result)


# ==========================================
# TEST 2: EMPTY DATASET
# ==========================================

print("\nTEST 2: EMPTY DATASET")

empty_data = pd.DataFrame()

result = validate_market_data(empty_data)

print(result)


# ==========================================
# TEST 3: MISSING VALUES
# ==========================================

print("\nTEST 3: MISSING VALUES")

missing_data = pd.DataFrame({
    "time": [1794369600, 1794370500],
    "open": [1.1000, None],
    "high": [1.1050, 1.1060],
    "low": [1.0980, 1.0990],
    "close": [1.1030, None]
})

result = validate_market_data(missing_data)

print(result)


# ==========================================
# TEST 4: INVALID INPUT TYPE
# ==========================================

print("\nTEST 4: INVALID INPUT TYPE")

invalid_data = "This is not market data"

result = validate_market_data(invalid_data)

print(result)

# ==========================================
# TEST 5: MARKET DATA WITHOUT DUPLICATES
# ==========================================

print("\nTEST 5: MARKET DATA WITHOUT DUPLICATES")

unique_data = pd.DataFrame({
    "time": [
        1794369600,
        1794370500,
        1794371400
    ],
    "open": [1.1000, 1.1010, 1.1020],
    "high": [1.1050, 1.1060, 1.1070],
    "low": [1.0980, 1.0990, 1.1000],
    "close": [1.1030, 1.1040, 1.1050]
})

result = validate_duplicate_candles(unique_data)

print(result)


# ==========================================
# TEST 6: MARKET DATA WITH DUPLICATES
# ==========================================

print("\nTEST 6: MARKET DATA WITH DUPLICATES")

duplicate_data = pd.DataFrame({
    "time": [
        1794369600,
        1794370500,
        1794370500,
        1794371400
    ],
    "open": [1.1000, 1.1010, 1.1015, 1.1020],
    "high": [1.1050, 1.1060, 1.1065, 1.1070],
    "low": [1.0980, 1.0990, 1.0995, 1.1000],
    "close": [1.1030, 1.1040, 1.1045, 1.1050]
})

result = validate_duplicate_candles(duplicate_data)

print(result)


# ==========================================
# TEST 7: MISSING TIMESTAMP COLUMN
# ==========================================

print("\nTEST 7: MISSING TIMESTAMP COLUMN")

no_time_data = pd.DataFrame({
    "open": [1.1000, 1.1010],
    "high": [1.1050, 1.1060],
    "low": [1.0980, 1.0990],
    "close": [1.1030, 1.1040]
})

result = validate_duplicate_candles(no_time_data)

print(result)



# ==========================================
# TEST 8: CORRECT CHRONOLOGICAL ORDER
# ==========================================

print("\nTEST 8: CORRECT CHRONOLOGICAL ORDER")

ordered_data = pd.DataFrame({
    "time": [
        1794369600,
        1794370500,
        1794371400,
        1794372300
    ],
    "open": [1.1000, 1.1010, 1.1020, 1.1030],
    "high": [1.1050, 1.1060, 1.1070, 1.1080],
    "low": [1.0980, 1.0990, 1.1000, 1.1010],
    "close": [1.1030, 1.1040, 1.1050, 1.1060]
})

result = validate_candle_order(ordered_data)

print(result)


# ==========================================
# TEST 9: INCORRECT CHRONOLOGICAL ORDER
# ==========================================

print("\nTEST 9: INCORRECT CHRONOLOGICAL ORDER")

unordered_data = pd.DataFrame({
    "time": [
        1794369600,
        1794371400,
        1794370500,
        1794372300
    ],
    "open": [1.1000, 1.1020, 1.1010, 1.1030],
    "high": [1.1050, 1.1070, 1.1060, 1.1080],
    "low": [1.0980, 1.1000, 1.0990, 1.1010],
    "close": [1.1030, 1.1050, 1.1040, 1.1060]
})

result = validate_candle_order(unordered_data)

print(result)


# ==========================================
# TEST 10: MISSING CANDLE TIMESTAMP
# ==========================================

print("\nTEST 10: MISSING CANDLE TIMESTAMP")

missing_time_data = pd.DataFrame({
    "time": [1794369600, None, 1794371400],
    "open": [1.1000, 1.1010, 1.1020],
    "high": [1.1050, 1.1060, 1.1070],
    "low": [1.0980, 1.0990, 1.1000],
    "close": [1.1030, 1.1040, 1.1050]
})

result = validate_candle_order(missing_time_data)
print(result)

# Tests 11–27: Test the following:
# OHLC price validation, 
# including invalid values and multiple candle errors.


# ==========================================
# TEST 11: VALID OHLC PRICE INTEGRITY
# ==========================================

print("\nTEST 11: VALID OHLC PRICES")

# Create a candle using the example prices we discussed.
valid_ohlc_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [1.10881],
    "close": [1.10886]
})

# Run the OHLC price integrity validator.
ohlc_result = validate_ohlc_prices(valid_ohlc_data)

print(ohlc_result)



# ==========================================
# TEST 12: HIGH PRICE LOWER THAN CLOSE
# ==========================================

print("\nTEST 12: HIGH PRICE LOWER THAN CLOSE")

# This candle is invalid because the Close
# is higher than the recorded High.
invalid_high_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10890],
    "low": [1.10881],
    "close": [1.10910]
})

# Run the OHLC validator.
invalid_high_result = validate_ohlc_prices(invalid_high_data)

print(invalid_high_result)



# ==========================================
# TEST 13: LOW PRICE HIGHER THAN CLOSE
# ==========================================

print("\nTEST 13: LOW PRICE HIGHER THAN CLOSE")

# This candle is invalid because the Low
# is higher than the recorded Close.
invalid_low_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [1.10900],
    "close": [1.10886]
})

# Run the OHLC validator.
invalid_low_result = validate_ohlc_prices(invalid_low_data)

print(invalid_low_result)



# ==========================================
# TEST 14: HIGH PRICE LOWER THAN LOW
# ==========================================

print("\nTEST 14: HIGH PRICE LOWER THAN LOW")

# This candle is invalid because its High
# is lower than its Low.
invalid_high_low_data = pd.DataFrame({
    "open": [1.10910],
    "high": [1.10890],
    "low": [1.10900],
    "close": [1.10905]
})

# Run the OHLC validator.
invalid_high_low_result = validate_ohlc_prices(
    invalid_high_low_data
)

print(invalid_high_low_result)



# ==========================================
# TEST 15: MISSING OHLC COLUMN
# ==========================================

print("\nTEST 15: MISSING OHLC COLUMN")

# This dataset is missing the Close column.
missing_ohlc_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [1.10881]
})

# Run the OHLC validator.
missing_ohlc_result = validate_ohlc_prices(
    missing_ohlc_data
)

print(missing_ohlc_result)



# ==========================================
# TEST 16: NON-NUMERIC OHLC PRICE
# ==========================================

print("\nTEST 16: NON-NUMERIC OHLC PRICE")

# This dataset contains text instead of a valid
# numerical High price.
nonnumeric_ohlc_data = pd.DataFrame({
    "open": [1.10914],
    "high": ["invalid"],
    "low": [1.10881],
    "close": [1.10886]
})



# Run the OHLC validator.
nonnumeric_ohlc_result = validate_ohlc_prices(
    nonnumeric_ohlc_data
)

print(nonnumeric_ohlc_result)



# ==========================================
# TEST 17: ZERO OR NEGATIVE OHLC PRICES
# ==========================================

print("\nTEST 17: ZERO OR NEGATIVE OHLC PRICES")

# This candle contains a zero Low price.
# ForexAI should reject it.
non_positive_ohlc_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [0.00000],
    "close": [1.10886]
})

# Run the OHLC validator using the Test 17 dataset.
non_positive_result = validate_ohlc_prices(
    non_positive_ohlc_data
)

print(non_positive_result)


# ==========================================
# TEST 18: INFINITE OHLC PRICES
# ==========================================

print("\nTEST 18: INFINITE OHLC PRICES")

# This candle contains an infinite High price.
# ForexAI should reject it.
infinite_ohlc_data = pd.DataFrame({
    "open": [1.10914],
    "high": [float("inf")],
    "low": [1.10881],
    "close": [1.10886]
})

# Run the OHLC validator.
infinite_result = validate_ohlc_prices(
    infinite_ohlc_data
)

print(infinite_result)

# ==========================================
# TEST 19: NEGATIVE INFINITE OHLC PRICE
# ==========================================

print("\nTEST 19: NEGATIVE INFINITE OHLC PRICE")

# This candle contains a negative infinite Low price.
# ForexAI should reject it.
negative_infinite_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [float("-inf")],
    "close": [1.10886]
})

# Run the OHLC validator.
negative_infinite_result = validate_ohlc_prices(
    negative_infinite_data
)

print(negative_infinite_result)

# ==========================================
# TEST 20: NEGATIVE OHLC PRICES
# ==========================================

print("\nTEST 20: NEGATIVE OHLC PRICES")

# This candle contains a negative Low price.
# ForexAI should reject it.
negative_ohlc_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [-1.10881],
    "close": [1.10886]
})

# Run the OHLC validator.
negative_result = validate_ohlc_prices(
    negative_ohlc_data
)

print(negative_result)

# ==========================================
# TEST 21: MULTIPLE INVALID OHLC PRICES
# ==========================================

print("\nTEST 21: MULTIPLE INVALID OHLC PRICES")

# This candle contains two invalid prices:
# High is negative and Low is zero.
multiple_invalid_data = pd.DataFrame({
    "open": [1.10914],
    "high": [-1.10939],
    "low": [0.0],
    "close": [1.10886]
})

# Run the OHLC validator.
multiple_invalid_result = validate_ohlc_prices(
    multiple_invalid_data
)

print(multiple_invalid_result)


# ==========================================
# TEST 22: OPEN PRICE ABOVE HIGH
# ==========================================

print("\nTEST 22: OPEN PRICE ABOVE HIGH")

# Open cannot be greater than High.
open_above_high_data = pd.DataFrame({
    "open": [1.11000],
    "high": [1.10939],
    "low": [1.10881],
    "close": [1.10886]
})

# Run the OHLC validator.
open_above_high_result = validate_ohlc_prices(
    open_above_high_data
)

print(open_above_high_result)

# ==========================================
# TEST 23: CLOSE PRICE ABOVE HIGH
# ==========================================

print("\nTEST 23: CLOSE PRICE ABOVE HIGH")

# Close cannot be greater than High.
close_above_high_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [1.10881],
    "close": [1.11000]
})

# Run the OHLC validator.
close_above_high_result = validate_ohlc_prices(
    close_above_high_data
)

print(close_above_high_result)


# ==========================================
# TEST 24: OPEN PRICE BELOW LOW
# ==========================================

print("\nTEST 24: OPEN PRICE BELOW LOW")

# Open cannot be lower than Low.
open_below_low_data = pd.DataFrame({
    "open": [1.10800],
    "high": [1.10939],
    "low": [1.10881],
    "close": [1.10886]
})

# Run the OHLC validator.
open_below_low_result = validate_ohlc_prices(
    open_below_low_data
)

print(open_below_low_result)

# ==========================================
# TEST 25: CLOSE PRICE BELOW LOW
# ==========================================

print("\nTEST 25: CLOSE PRICE BELOW LOW")

# Close cannot be lower than Low.
close_below_low_data = pd.DataFrame({
    "open": [1.10914],
    "high": [1.10939],
    "low": [1.10881],
    "close": [1.10800]
})

# Run the OHLC validator.
close_below_low_result = validate_ohlc_prices(
    close_below_low_data
)

print(close_below_low_result)

# ==========================================
# TEST 26: MULTIPLE CANDLES WITH ONE INVALID
# ==========================================

print("\nTEST 26: MULTIPLE CANDLES WITH ONE INVALID")

# Three candles: the first two are valid.
# The third contains an invalid High price.
multiple_candles_data = pd.DataFrame({
    "open": [1.10914, 1.10890, 1.10920],
    "high": [1.10939, 1.10920, 1.10880],
    "low": [1.10881, 1.10860, 1.10850],
    "close": [1.10886, 1.10910, 1.10900]
})

# Run the OHLC validator.
multiple_candles_result = validate_ohlc_prices(
    multiple_candles_data
)

print(multiple_candles_result)

# ==========================================
# TEST 27: MULTIPLE INVALID CANDLES
# ==========================================

print("\nTEST 27: MULTIPLE INVALID CANDLES")

# The second and fourth candles are invalid.
multiple_invalid_candles = pd.DataFrame({
    "open":  [1.10914, 1.10890, 1.10920, 1.10910],
    "high":  [1.10939, 1.10880, 1.10940, 1.10930],
    "low":   [1.10881, 1.10860, 1.10890, 1.10920],
    "close": [1.10886, 1.10910, 1.10920, 1.10900]
})

# Run the OHLC validator.
multiple_invalid_candles_result = validate_ohlc_prices(
    multiple_invalid_candles
)

print(multiple_invalid_candles_result)

# Tests 28–29: Tests the following:
# Actual EURUSD market data retrieved 
# from MT5 passed complete validation.


# ==========================================
# TEST 28: VALIDATE ACTUAL MT5 MARKET DATA
# ==========================================

print("\nTEST 28: ACTUAL MT5 MARKET DATA")

# Retrieve 100 completed EURUSD M15 candles.
market_data = get_historical_data(
    "EURUSD",
    mt5.TIMEFRAME_M15,
    100
)

# Confirm that market data was retrieved.
if market_data is None or market_data.empty:

    print("TEST 28 FAILED: No market data was retrieved.")

else:

    # Run all validation checks through the
    # centralized market-data validator.
    result = validate_market_data(market_data)

    # Display the complete validation result.
    print("\nCOMPLETE VALIDATION RESULT:")
    print(result)

    # Confirm whether the actual MT5 data passed.
    if result["valid"]:

        print(
            "\nTEST 28 PASSED: "
            "Actual MT5 market data is valid."
        )

    else:

        print(
            "\nTEST 28 FAILED: "
            "Market-data validation errors detected."
        )
        
                
# ==========================================
# TEST 29: COMPLETE MARKET DATA VALIDATION
# ==========================================

print("\nTEST 29: COMPLETE MARKET DATA VALIDATION")

# Retrieve 100 completed EURUSD M15 candles.
market_data = get_historical_data(
    "EURUSD",
    mt5.TIMEFRAME_M15,
    100
)

# Confirm that market data was retrieved.
if market_data is None or market_data.empty:

    print("TEST 29 FAILED: No market data retrieved.")

else:

    # Run the central validation function.
    result = validate_market_data(market_data)

    # Display the combined validation result.
    print("\nCOMPLETE VALIDATION RESULT:")
    print(result)

    # Determine whether the complete dataset passed.
    if result["valid"]:
        print("\nTEST 29 PASSED: All validation checks succeeded.")

    else:
        print("\nTEST 29 FAILED: Validation errors detected.")
        

# Test 30: Tests the following:
# The validator correctly identified 
# four separate problems in one corrupted dataset.

# ==========================================
# TEST 30: MULTIPLE MARKET DATA ERRORS
# ==========================================

print("\nTEST 30: MULTIPLE MARKET DATA ERRORS")

# Create a dataset containing several problems.
corrupted_market_data = pd.DataFrame({

    # The second and third candles share a timestamp.
    # The timestamps are also out of chronological order.
    "time": pd.to_datetime([
        "2026-11-12 01:00:00",
        "2026-11-12 02:00:00",
        "2026-11-12 02:00:00",
        "2026-11-12 00:00:00"
    ], utc=True),

    "open":  [1.10914, 1.10890, 1.10920, 1.10910],
    "high":  [1.10939, 1.10880, 1.10940, 1.10930],
    "low":   [1.10881, 1.10860, 1.10890, 1.10920],
    "close": [1.10886, 1.10910, 1.10920, 1.10900]
})

# Run the central market-data validator.
result = validate_market_data(corrupted_market_data)

# Display the combined validation result.
print("\nCORRUPTED DATA VALIDATION RESULT:")
print(result)

# Confirm that the invalid dataset was rejected.
if not result["valid"]:
    print("\nTEST 30 PASSED: Multiple data errors detected.")

else:
    print("\nTEST 30 FAILED: Corrupted data was accepted.")
    


print("\n=== DATA VALIDATOR TEST FINISHED ===")