import pandas as pd
from analysis.technical_indicators import calculate_ema, calculate_rsi,  calculate_atr
import numpy as np

# ==========================================
# FOREXAI: TECHNICAL INDICATOR TESTS
# ==========================================


# ==========================================
# EXPONENTIAL MOVING AVERAGE (EMA) TESTS
# ==========================================

print("\nTEST 1: EMA CALCULATION")

# Create sample closing prices.
closing_prices = pd.Series(
    [10.0, 11.0, 12.0, 13.0, 14.0]
)

# Calculate the 3-period EMA.
ema_result = calculate_ema(
    closing_prices,
    period=3
)

# Expected values using the EMA recurrence
# with alpha = 2 / (period + 1) = 0.5.
expected_ema = [
    None,
    None,
    11.25,
    12.125,
    13.0625
]

# Compare the calculated values with the expected values.
for actual, expected in zip(ema_result, expected_ema):

    if expected is None:
        assert pd.isna(actual), (
            "EMA should not produce a value before "
            "the minimum period is reached."
        )

    else:
        assert abs(actual - expected) < 0.000001, (
            f"EMA mismatch: expected {expected}, got {actual}"
        )

print("Calculated EMA values:")

for index, value in ema_result.items():

    if pd.isna(value):
        print(f"{index}: Not enough data")

    else:
        print(f"{index}: {value:.4f}")

print("TEST 1 PASSED: EMA calculation is correct.")



print("\nTEST 2: INVALID EMA INPUT TYPE")

# Attempt to calculate EMA using a list instead of a Pandas Series.
try:
    calculate_ema([10.0, 11.0, 12.0], period=3)

    raise AssertionError(
        "EMA should reject input that is not a Pandas Series."
    )

except TypeError as error:
    print(f"Expected error received: {error}")

print("TEST 2 PASSED: Invalid input type rejected.")


print("\nTEST 3: INVALID EMA PERIOD")

# Attempt to calculate EMA using a zero period.
try:
    calculate_ema(
        pd.Series([10.0, 11.0, 12.0]),
        period=0
    )

    raise AssertionError(
        "EMA should reject a zero period."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 3 PASSED: Invalid EMA period rejected.")



print("\nTEST 4: NEGATIVE EMA PERIOD")

# Attempt to calculate EMA using a negative period.
try:
    calculate_ema(
        pd.Series([10.0, 11.0, 12.0]),
        period=-5
    )

    raise AssertionError(
        "EMA should reject a negative period."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 4 PASSED: Negative EMA period rejected.")



print("\nTEST 5: EMPTY EMA INPUT")

# Attempt to calculate EMA using an empty Pandas Series.
try:
    calculate_ema(
        pd.Series(dtype=float),
        period=3
    )

    raise AssertionError(
        "EMA should reject an empty price series."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 5 PASSED: Empty EMA input rejected.")



print("\nTEST 6: MISSING EMA PRICE VALUES")

# Create sample prices containing a missing value.
incomplete_prices = pd.Series(
    [10.0, 11.0, None, 13.0, 14.0]
)

# Attempt to calculate EMA using incomplete prices.
try:
    calculate_ema(
        incomplete_prices,
        period=3
    )

    raise AssertionError(
        "EMA should reject missing price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 6 PASSED: Missing EMA prices rejected.")


print("\nTEST 7: NON-NUMERIC EMA PRICE VALUES")

# Create sample prices containing non-numeric text.
invalid_prices = pd.Series(
    [10.0, 11.0, "invalid", 13.0, 14.0]
)

# Attempt to calculate EMA using invalid prices.
try:
    calculate_ema(
        invalid_prices,
        period=3
    )

    raise AssertionError(
        "EMA should reject non-numeric price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 7 PASSED: Non-numeric EMA prices rejected.")


print("\nTEST 8: INSUFFICIENT EMA HISTORY")

# Supply only two closing prices for a 3-period EMA.
short_price_history = pd.Series(
    [10.0, 11.0]
)

# Calculate the EMA.
short_ema = calculate_ema(
    short_price_history,
    period=3
)

# Confirm that no EMA values are produced.
assert short_ema.isnull().all(), (
    "EMA should not produce values when "
    "there are fewer candles than the requested period."
)

print("EMA result:")
print("Not enough data")

print("TEST 8 PASSED: Insufficient EMA history handled correctly.")



print("\nTEST 9: INFINITE EMA PRICE VALUES")

# Create sample prices containing an infinite value.
infinite_prices = pd.Series(
    [10.0, 11.0, float("inf"), 13.0, 14.0]
)

# Attempt to calculate EMA using infinite prices.
try:
    calculate_ema(
        infinite_prices,
        period=3
    )

    raise AssertionError(
        "EMA should reject infinite price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 9 PASSED: Infinite EMA prices rejected.")



print("\nTEST 10: NEGATIVE INFINITE EMA PRICE")

# Create sample prices containing negative infinity.
negative_infinite_prices = pd.Series(
    [10.0, 11.0, float("-inf"), 13.0, 14.0]
)

# Attempt to calculate EMA using negative infinity.
try:
    calculate_ema(
        negative_infinite_prices,
        period=3
    )

    raise AssertionError(
        "EMA should reject negative infinite prices."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 10 PASSED: Negative infinite EMA prices rejected.")


print("\nTEST 11: INVALID EMA PERIOD TYPE")

# Attempt to calculate EMA using a decimal period.
try:
    calculate_ema(
        pd.Series([10.0, 11.0, 12.0, 13.0]),
        period=3.5
    )

    raise AssertionError(
        "EMA should reject decimal periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 11 PASSED: Decimal EMA periods rejected.")

print("\nTEST 12: BOOLEAN EMA PERIOD")

# Attempt to calculate EMA using True as the period.
try:
    calculate_ema(
        pd.Series([10.0, 11.0, 12.0, 13.0]),
        period=True
    )

    raise AssertionError(
        "EMA should reject Boolean periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 12 PASSED: Boolean EMA periods rejected.")


# ------------------------------------------

# ==========================================
# RELATIVE STRENGTH INDEX (RSI) TESTS
# ==========================================

print("\nTEST 13: RSI CALCULATION")
print("\nTest 13: Continuous gains → RSI 100.")

# Create sample closing prices with consistent upward movement.
rsi_closing_prices = pd.Series(
    [10.0, 11.0, 12.0, 13.0, 14.0,
     15.0, 16.0, 17.0, 18.0, 19.0,
     20.0, 21.0, 22.0, 23.0, 24.0]
)

# Calculate the 14-period RSI.
rsi_result = calculate_rsi(
    rsi_closing_prices,
    period=14
)

# Confirm that the RSI reaches 100 when there are gains
# and no losses.
assert rsi_result.iloc[-1] == 100, (
    "RSI should equal 100 when there are gains "
    "and no losses."
)

print("Calculated RSI values:")
print(rsi_result)

print("TEST 13 PASSED: RSI calculation completed correctly.")

print("\nTEST 14: RSI WITH CONSISTENT LOSSES")
print("\nTest 14: Continuous losses → RSI 0.")
# Create sample closing prices with consistent downward movement.
falling_prices = pd.Series(
    [24.0, 23.0, 22.0, 21.0, 20.0,
     19.0, 18.0, 17.0, 16.0, 15.0,
     14.0, 13.0, 12.0, 11.0, 10.0]
)

# Calculate the 14-period RSI.
falling_rsi = calculate_rsi(
    falling_prices,
    period=14
)

# Confirm that RSI equals zero when there are losses
# and no gains.
assert falling_rsi.iloc[-1] == 0, (
    "RSI should equal 0 when there are losses "
    "and no gains."
)

print("Calculated RSI:")
print(falling_rsi)

print("TEST 14 PASSED: RSI correctly identifies consistent losses.")

print("\nTEST 15: RSI WITH NO PRICE MOVEMENT")

# Create closing prices that remain unchanged.
unchanged_prices = pd.Series(
    [10.0] * 15
)

# Calculate the 14-period RSI.
unchanged_rsi = calculate_rsi(
    unchanged_prices,
    period=14
)

# Confirm that RSI equals 50 when there are no gains or losses.
assert unchanged_rsi.iloc[-1] == 50, (
    "RSI should equal 50 when there are no gains "
    "and no losses."
)

print("Calculated RSI:")
print(unchanged_rsi)

print("TEST 15 PASSED: RSI correctly handles no price movement.")


print("\nTEST 16: INSUFFICIENT RSI HISTORY")

# Supply only 14 closing prices for a 14-period RSI.
short_rsi_history = pd.Series(
    [10.0, 11.0, 12.0, 13.0,
     14.0, 15.0, 16.0, 17.0,
     18.0, 19.0, 20.0, 21.0,
     22.0, 23.0]
)

# Attempt to calculate RSI with insufficient history.
try:
    calculate_rsi(
        short_rsi_history,
        period=14
    )

    raise AssertionError(
        "RSI should reject insufficient historical data."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 16 PASSED: Insufficient RSI history rejected.")

print("\nTEST 17: INVALID RSI INPUT TYPE")

# Attempt to calculate RSI using a list instead of a Pandas Series.
try:
    calculate_rsi(
        [10.0, 11.0, 12.0, 13.0, 14.0],
        period=3
    )

    raise AssertionError(
        "RSI should reject input that is not a Pandas Series."
    )

except TypeError as error:
    print(f"Expected error received: {error}")

print("TEST 17 PASSED: Invalid RSI input type rejected.")


print("\nTEST 18: ZERO RSI PERIOD")

# Attempt to calculate RSI using a zero period.
try:
    calculate_rsi(
        pd.Series([10.0, 11.0, 12.0, 13.0]),
        period=0
    )

    raise AssertionError(
        "RSI should reject a zero period."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 18 PASSED: Zero RSI period rejected.")



print("\nTEST 19: NEGATIVE RSI PERIOD")

# Attempt to calculate RSI using a negative period.
try:
    calculate_rsi(
        pd.Series([10.0, 11.0, 12.0, 13.0]),
        period=-5
    )

    raise AssertionError(
        "RSI should reject a negative period."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 19 PASSED: Negative RSI period rejected.")


print("\nTEST 20: EMPTY RSI INPUT")

# Attempt to calculate RSI using an empty Pandas Series.
try:
    calculate_rsi(
        pd.Series(dtype=float),
        period=14
    )

    raise AssertionError(
        "RSI should reject an empty price series."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 20 PASSED: Empty RSI input rejected.")

print("\nTEST 21: MISSING RSI PRICE VALUES")

# Create sample prices containing a missing value.
incomplete_rsi_prices = pd.Series(
    [10.0, 11.0, 12.0, None, 14.0,
     15.0, 16.0, 17.0, 18.0, 19.0,
     20.0, 21.0, 22.0, 23.0, 24.0]
)

# Attempt to calculate RSI using incomplete prices.
try:
    calculate_rsi(
        incomplete_rsi_prices,
        period=14
    )

    raise AssertionError(
        "RSI should reject missing price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 21 PASSED: Missing RSI prices rejected.")

print("\nTEST 22: NON-NUMERIC RSI PRICE VALUES")

# Create sample prices containing non-numeric text.
invalid_rsi_prices = pd.Series(
    [10.0, 11.0, 12.0, "invalid", 14.0,
     15.0, 16.0, 17.0, 18.0, 19.0,
     20.0, 21.0, 22.0, 23.0, 24.0]
)

# Attempt to calculate RSI using invalid prices.
try:
    calculate_rsi(
        invalid_rsi_prices,
        period=14
    )

    raise AssertionError(
        "RSI should reject non-numeric price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 22 PASSED: Non-numeric RSI prices rejected.")


print("\nTEST 23: POSITIVE INFINITE RSI PRICE")

# Create sample prices containing positive infinity.
infinite_rsi_prices = pd.Series(
    [10.0, 11.0, 12.0, 13.0, 14.0,
     15.0, 16.0, 17.0, 18.0, 19.0,
     20.0, 21.0, 22.0, float("inf"), 24.0]
)

# Attempt to calculate RSI using infinite prices.
try:
    calculate_rsi(
        infinite_rsi_prices,
        period=14
    )

    raise AssertionError(
        "RSI should reject positive infinite prices."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 23 PASSED: Positive infinite RSI prices rejected.")

# ==========================================
# TEST 24: NEGATIVE INFINITE RSI PRICE
# ==========================================

print("\nTEST 24: NEGATIVE INFINITE RSI PRICE")

# Create RSI test data containing a negative infinite price.
test_data = pd.Series(
    [100, 102, 104, 106, 108, 110, 112, 114, 116, 118,
     120, 122, 124, 126, -np.inf]
)

try:
    calculate_rsi(test_data, period=14)

except ValueError as error:

    # Confirm that the expected infinite-value error was received.
    assert str(error) == (
        "RSI input contains infinite price values."
    )

    print(f"Expected error received: {error}")
    print("TEST 24 PASSED: Negative infinite RSI prices rejected.")

else:
    raise AssertionError(
        "RSI should reject negative infinite price values."
    )
    
# ==========================================
# TEST 25: INVALID RSI PERIOD TYPE
# ==========================================

print("\nTEST 25: INVALID RSI PERIOD TYPE")

# Attempt to calculate RSI using a decimal period.
try:
    calculate_rsi(
        pd.Series([10.0, 11.0, 12.0, 13.0, 14.0]),
        period=3.5
    )

    raise AssertionError(
        "RSI should reject decimal periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 25 PASSED: Decimal RSI periods rejected.")


# ==========================================
# TEST 26: BOOLEAN RSI PERIOD
# ==========================================

print("\nTEST 26: BOOLEAN RSI PERIOD")

# Attempt to calculate RSI using True as the period.
try:
    calculate_rsi(
        pd.Series([10.0, 11.0, 12.0, 13.0, 14.0]),
        period=True
    )

    raise AssertionError(
        "RSI should reject Boolean periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 26 PASSED: Boolean RSI periods rejected.")


# ==========================================
# TEST 27: ATR CALCULATION
# ==========================================

print("\nTEST 27: ATR CALCULATION")

# Create sample OHLC market data.
test_data = pd.DataFrame({
    "High": [
        12, 13, 14, 15, 16,
        17, 18, 19, 20, 21,
        22, 23, 24, 25, 26
    ],
    "Low": [
        10, 11, 12, 13, 14,
        15, 16, 17, 18, 19,
        20, 21, 22, 23, 24
    ],
    "Close": [
        11, 12, 13, 14, 15,
        16, 17, 18, 19, 20,
        21, 22, 23, 24, 25
    ]
})

# Calculate the 14-period ATR.
atr_result = calculate_atr(
    test_data,
    period=14
)

# Every candle has a True Range of 2.
# Therefore, the initial 14-period ATR should equal 2.
assert pd.isna(atr_result.iloc[:13]).all(), (
    "ATR should not produce values before "
    "the minimum period is reached."
)

assert np.isclose(atr_result.iloc[13], 2.0), (
    "Initial ATR calculation is incorrect."
)

assert np.isclose(atr_result.iloc[14], 2.0), (
    "Wilder's ATR smoothing calculation is incorrect."
)

print("TEST 27 PASSED: ATR calculation is correct.")


# ==========================================
# TEST 28: INVALID ATR INPUT TYPE
# ==========================================

print("\nTEST 28: INVALID ATR INPUT TYPE")

# Attempt to calculate ATR using a Pandas Series.
try:
    calculate_atr(
        pd.Series([10.0, 11.0, 12.0, 13.0, 14.0]),
        period=3
    )

    raise AssertionError(
        "ATR should reject Pandas Series input."
    )

except TypeError as error:
    print(f"Expected error received: {error}")

print("TEST 28 PASSED: Invalid ATR input types rejected.")


# ==========================================
# TEST 29: ZERO ATR PERIOD
# ==========================================

print("\nTEST 29: ZERO ATR PERIOD")

# Create valid sample OHLC data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0],
    "Low": [10.0, 11.0, 12.0],
    "Close": [11.0, 12.0, 13.0]
})

# Attempt to calculate ATR using a zero period.
try:
    calculate_atr(
        test_data,
        period=0
    )

    raise AssertionError(
        "ATR should reject a zero period."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 29 PASSED: Zero ATR periods rejected.")


# ==========================================
# TEST 30: NEGATIVE ATR PERIOD
# ==========================================

print("\nTEST 30: NEGATIVE ATR PERIOD")

# Create valid sample OHLC data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0],
    "Low": [10.0, 11.0, 12.0],
    "Close": [11.0, 12.0, 13.0]
})

# Attempt to calculate ATR using a negative period.
try:
    calculate_atr(
        test_data,
        period=-3
    )

    raise AssertionError(
        "ATR should reject negative periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 30 PASSED: Negative ATR periods rejected.")


# ==========================================
# TEST 31: INVALID ATR PERIOD TYPE
# ==========================================

print("\nTEST 31: INVALID ATR PERIOD TYPE")

# Create valid sample OHLC data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0, 16.0],
    "Low": [10.0, 11.0, 12.0, 13.0, 14.0],
    "Close": [11.0, 12.0, 13.0, 14.0, 15.0]
})

# Attempt to calculate ATR using a decimal period.
try:
    calculate_atr(
        test_data,
        period=3.5
    )

    raise AssertionError(
        "ATR should reject decimal periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 31 PASSED: Decimal ATR periods rejected.")


# ==========================================
# TEST 32: BOOLEAN ATR PERIOD
# ==========================================

print("\nTEST 32: BOOLEAN ATR PERIOD")

# Create valid sample OHLC data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0, 16.0],
    "Low": [10.0, 11.0, 12.0, 13.0, 14.0],
    "Close": [11.0, 12.0, 13.0, 14.0, 15.0]
})

# Attempt to calculate ATR using True as the period.
try:
    calculate_atr(
        test_data,
        period=True
    )

    raise AssertionError(
        "ATR should reject Boolean periods."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 32 PASSED: Boolean ATR periods rejected.")


# ==========================================
# TEST 33: EMPTY ATR INPUT
# ==========================================

print("\nTEST 33: EMPTY ATR INPUT")

# Create an empty DataFrame with the required columns.
test_data = pd.DataFrame(
    columns=["High", "Low", "Close"]
)

# Attempt to calculate ATR using empty data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject empty market data."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 33 PASSED: Empty ATR input rejected.")


# ==========================================
# TEST 34: MISSING ATR COLUMNS
# ==========================================

print("\nTEST 34: MISSING ATR COLUMNS")

# Create market data without the required Close column.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0],
    "Low": [10.0, 11.0, 12.0]
})

# Attempt to calculate ATR using incomplete market data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject missing required columns."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 34 PASSED: Missing ATR columns rejected.")


# ==========================================
# TEST 35: MISSING ATR PRICE VALUES
# ==========================================

print("\nTEST 35: MISSING ATR PRICE VALUES")

# Create OHLC data containing a missing High value.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, np.nan, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using incomplete price data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject missing price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 35 PASSED: Missing ATR price values rejected.")


# ==========================================
# TEST 36: NON-NUMERIC ATR PRICE VALUES
# ==========================================

print("\nTEST 36: NON-NUMERIC ATR PRICE VALUES")

# Create OHLC data containing a non-numeric High value.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, "invalid", 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using invalid price data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject non-numeric price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 36 PASSED: Non-numeric ATR price values rejected.")


# ==========================================
# TEST 37: POSITIVE INFINITY ATR PRICE VALUES
# ==========================================

print("\nTEST 37: POSITIVE INFINITY ATR PRICE VALUES")

# Create OHLC data containing a positive infinity value.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, np.inf, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using infinite price data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject positive infinity values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 37 PASSED: Positive infinity ATR price values rejected.")


# ==========================================
# TEST 38: NEGATIVE INFINITY ATR PRICE VALUES
# ==========================================

print("\nTEST 38: NEGATIVE INFINITY ATR PRICE VALUES")

# Create OHLC data containing a negative infinity value.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, -np.inf, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using infinite price data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject negative infinity values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 38 PASSED: Negative infinity ATR price values rejected.")


# ==========================================
# TEST 39: HIGH PRICE BELOW LOW PRICE
# ==========================================

print("\nTEST 39: HIGH PRICE BELOW LOW PRICE")

# Create OHLC data containing an invalid candle.
test_data = pd.DataFrame({
    "High": [12.0, 10.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using invalid candle data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject High prices below Low prices."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 39 PASSED: High prices below Low prices rejected.")

# ==========================================
# TEST 40: CLOSE PRICE BELOW LOW PRICE
# ==========================================

print("\nTEST 40: CLOSE PRICE BELOW LOW PRICE")

# Create OHLC data containing an invalid Close price.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 11.0, 14.0]
})

# Attempt to calculate ATR using invalid candle data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject Close prices below Low prices."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 40 PASSED: Close prices below Low prices rejected.")


# ==========================================
# TEST 41: CLOSE PRICE ABOVE HIGH PRICE
# ==========================================

print("\nTEST 41: CLOSE PRICE ABOVE HIGH PRICE")

# Create OHLC data containing an invalid Close price.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 15.0, 14.0]
})

# Attempt to calculate ATR using invalid candle data.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject Close prices above High prices."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 41 PASSED: Close prices above High prices rejected.")


# ==========================================
# TEST 42: ZERO ATR PRICE VALUES
# ==========================================

print("\nTEST 42: ZERO ATR PRICE VALUES")

# Create OHLC data containing a zero price.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 0.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using a zero price.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject zero price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 42 PASSED: Zero ATR price values rejected.")


# ==========================================
# TEST 43: NEGATIVE ATR PRICE VALUES
# ==========================================

print("\nTEST 43: NEGATIVE ATR PRICE VALUES")

# Create OHLC data containing a negative price.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, -2.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Attempt to calculate ATR using a negative price.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject negative price values."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 43 PASSED: Negative ATR price values rejected.")


# ==========================================
# TEST 44: INSUFFICIENT ATR HISTORICAL DATA
# ==========================================

print("\nTEST 44: INSUFFICIENT ATR HISTORICAL DATA")

# Create valid OHLC data with fewer candles than the ATR period.
test_data = pd.DataFrame({
    "High": [12.0, 13.0],
    "Low": [10.0, 11.0],
    "Close": [11.0, 12.0]
})

# Attempt to calculate ATR without enough historical candles.
try:
    calculate_atr(
        test_data,
        period=3
    )

    raise AssertionError(
        "ATR should reject insufficient historical data."
    )

except ValueError as error:
    print(f"Expected error received: {error}")

print("TEST 44 PASSED: Insufficient ATR historical data rejected.")


# ==========================================
# TEST 45: ATR TRUE RANGE PRICE GAPS
# ==========================================

print("\nTEST 45: ATR TRUE RANGE PRICE GAPS")

# Create OHLC data containing a gap between candles.
test_data = pd.DataFrame({
    "High": [12.0, 15.0, 16.0],
    "Low": [10.0, 13.0, 14.0],
    "Close": [10.0, 14.0, 15.0]
})

# Calculate ATR using a period of 2.
atr = calculate_atr(
    test_data,
    period=2
)

# The first True Range is 2.
# The second True Range is 5 because of the price gap.
# Initial ATR = (2 + 5) / 2 = 3.5.
expected_atr = 3.5

# Confirm that the calculated ATR accounts for the gap.
assert np.isclose(
    atr.iloc[1],
    expected_atr
), "ATR failed to account for the price gap."

print("TEST 45 PASSED: ATR correctly accounts for price gaps.")


# ==========================================
# TEST 46: WILDER'S ATR SMOOTHING ACCURACY
# ==========================================

print("\nTEST 46: WILDER'S ATR SMOOTHING ACCURACY")

# Create OHLC data with changing True Range values.
test_data = pd.DataFrame({
    "High": [12.0, 14.0, 17.0, 18.0],
    "Low": [10.0, 11.0, 13.0, 14.0],
    "Close": [11.0, 13.0, 16.0, 17.0]
})

# Calculate ATR using a period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Expected True Range values:
# Candle 1: 2
# Candle 2: 3
# Candle 3: 4
# Candle 4: 4

# Initial ATR = (2 + 3 + 4) / 3 = 3.
expected_initial_atr = 3.0

# Next ATR = ((3 * 2) + 4) / 3 = 10/3.
expected_next_atr = 10.0 / 3.0

# Verify the initial ATR calculation.
assert np.isclose(
    atr.iloc[2],
    expected_initial_atr
), "Initial ATR calculation is incorrect."

# Verify Wilder's subsequent smoothing calculation.
assert np.isclose(
    atr.iloc[3],
    expected_next_atr
), "Wilder's ATR smoothing calculation is incorrect."

print("TEST 46 PASSED: Wilder's ATR smoothing is correct.")


# ==========================================
# TEST 47: ATR INDEX PRESERVATION
# ==========================================

print("\nTEST 47: ATR INDEX PRESERVATION")

# Create OHLC data with a custom index.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
}, index=[100, 101, 102, 103])

# Calculate ATR using a period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Confirm that ATR preserves the original index.
assert atr.index.equals(
    test_data.index
), "ATR failed to preserve the original DataFrame index."

print("TEST 47 PASSED: ATR preserves the original DataFrame index.")


# ==========================================
# TEST 48: ATR INPUT DATA IMMUTABILITY
# ==========================================

print("\nTEST 48: ATR INPUT DATA IMMUTABILITY")

# Create sample OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Save an independent copy of the original data.
original_data = test_data.copy(deep=True)

# Calculate ATR.
calculate_atr(
    test_data,
    period=3
)

# Confirm that the original DataFrame remains unchanged.
pd.testing.assert_frame_equal(
    test_data,
    original_data
)

print("TEST 48 PASSED: ATR does not modify the original DataFrame.")


# ==========================================
# TEST 49: DEFAULT ATR PERIOD
# ==========================================

print("\nTEST 49: DEFAULT ATR PERIOD")

# Create 15 candles of valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0] * 15,
    "Low": [10.0] * 15,
    "Close": [11.0] * 15
})

# Calculate ATR without specifying a period.
atr = calculate_atr(test_data)

# Confirm that the first 13 values are NaN.
assert atr.iloc[:13].isna().all(), (
    "ATR should return NaN for the first 13 candles."
)

# Confirm that the 14th candle produces an ATR value.
assert np.isclose(atr.iloc[13], 2.0), (
    "Default ATR period should be 14."
)

# Confirm that the 15th candle also produces an ATR value.
assert np.isclose(atr.iloc[14], 2.0), (
    "Default ATR calculation is incorrect."
)

print("TEST 49 PASSED: Default ATR period of 14 works correctly.")


# ==========================================
# TEST 50: CUSTOM ATR PERIOD
# ==========================================

print("\nTEST 50: CUSTOM ATR PERIOD")

# Create 6 candles of valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0] * 6,
    "Low": [10.0] * 6,
    "Close": [11.0] * 6
})

# Calculate ATR using a custom period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Confirm that the first 2 values are NaN.
assert atr.iloc[:2].isna().all(), (
    "ATR should return NaN for the first 2 candles."
)

# Confirm that the third candle produces an ATR value.
assert np.isclose(atr.iloc[2], 2.0), (
    "Custom ATR period calculation is incorrect."
)

# Confirm that subsequent ATR values are calculated.
assert atr.iloc[3:].notna().all(), (
    "ATR should calculate values after the initial period."
)

print("TEST 50 PASSED: Custom ATR periods work correctly.")


# ==========================================
# TEST 51: MINIMUM ATR HISTORICAL DATA
# ==========================================

print("\nTEST 51: MINIMUM ATR HISTORICAL DATA")

# Create exactly 14 candles of valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0] * 14,
    "Low": [10.0] * 14,
    "Close": [11.0] * 14
})

# Calculate ATR using exactly 14 candles.
atr = calculate_atr(
    test_data,
    period=14
)

# Confirm that the first 13 values are NaN.
assert atr.iloc[:13].isna().all(), (
    "The first 13 ATR values should be NaN."
)

# Confirm that the 14th candle produces a valid ATR.
assert np.isclose(atr.iloc[13], 2.0), (
    "ATR should calculate with exactly 14 candles."
)

print("TEST 51 PASSED: Minimum ATR historical data accepted.")


# ==========================================
# TEST 52: ATR OUTPUT DATA TYPE
# ==========================================

print("\nTEST 52: ATR OUTPUT DATA TYPE")

# Create valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Calculate ATR.
atr = calculate_atr(
    test_data,
    period=3
)

# Confirm that ATR returns a Pandas Series.
assert isinstance(atr, pd.Series), (
    "ATR output must be a Pandas Series."
)

print("TEST 52 PASSED: ATR returns a Pandas Series.")


# ==========================================
# TEST 53: ATR OUTPUT NUMERIC DATA TYPE
# ==========================================

print("\nTEST 53: ATR OUTPUT NUMERIC DATA TYPE")

# Create valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0],
    "Low": [10.0, 11.0, 12.0, 13.0],
    "Close": [11.0, 12.0, 13.0, 14.0]
})

# Calculate ATR.
atr = calculate_atr(
    test_data,
    period=3
)

# Confirm that ATR values use a floating-point data type.
assert pd.api.types.is_float_dtype(atr.dtype), (
    "ATR output must use a floating-point data type."
)

print("TEST 53 PASSED: ATR output uses a floating-point data type.")


# ==========================================
# TEST 54: ATR OUTPUT FINITE VALUES
# ==========================================

print("\nTEST 54: ATR OUTPUT FINITE VALUES")

# Create valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0, 16.0],
    "Low": [10.0, 11.0, 12.0, 13.0, 14.0],
    "Close": [11.0, 12.0, 13.0, 14.0, 15.0]
})

# Calculate ATR using a period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Extract calculated ATR values, excluding initial NaN values.
valid_atr = atr.dropna()

# Confirm that all calculated ATR values are finite.
assert np.isfinite(valid_atr).all(), (
    "ATR output must not contain infinite values."
)

print("TEST 54 PASSED: ATR output contains only finite calculated values.")


# ==========================================
# TEST 55: ATR OUTPUT NON-NEGATIVE VALUES
# ==========================================

print("\nTEST 55: ATR OUTPUT NON-NEGATIVE VALUES")

# Create valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0, 16.0],
    "Low": [10.0, 11.0, 12.0, 13.0, 14.0],
    "Close": [11.0, 12.0, 13.0, 14.0, 15.0]
})

# Calculate ATR using a period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Extract calculated ATR values, excluding initial NaN values.
valid_atr = atr.dropna()

# Confirm that all calculated ATR values are non-negative.
assert (valid_atr >= 0).all(), (
    "ATR output must contain non-negative values."
)

print("TEST 55 PASSED: ATR output contains only non-negative values.")


# ==========================================
# TEST 56: ATR OUTPUT LENGTH ALIGNMENT
# ==========================================

print("\nTEST 56: ATR OUTPUT LENGTH ALIGNMENT")

# Create valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0, 16.0],
    "Low": [10.0, 11.0, 12.0, 13.0, 14.0],
    "Close": [11.0, 12.0, 13.0, 14.0, 15.0]
})

# Calculate ATR using a period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Confirm that ATR contains the same number of rows as the input.
assert len(atr) == len(test_data), (
    "ATR output length must match the input DataFrame length."
)

print("TEST 56 PASSED: ATR output length matches the input data.")


# ==========================================
# TEST 57: ATR INITIAL NaN VALUES
# ==========================================

print("\nTEST 57: ATR INITIAL NaN VALUES")

# Create valid OHLC market data.
test_data = pd.DataFrame({
    "High": [12.0, 13.0, 14.0, 15.0, 16.0],
    "Low": [10.0, 11.0, 12.0, 13.0, 14.0],
    "Close": [11.0, 12.0, 13.0, 14.0, 15.0]
})

# Calculate ATR using a period of 3.
atr = calculate_atr(
    test_data,
    period=3
)

# Confirm that the first 2 positions contain NaN.
assert atr.iloc[:2].isna().all(), (
    "The first period - 1 ATR values must be NaN."
)

# Confirm that the third position contains a valid ATR.
assert pd.notna(atr.iloc[2]), (
    "The first ATR value should appear at the period boundary."
)

print("TEST 57 PASSED: ATR initial NaN values are correctly positioned.")


# ==========================================
# TEST 58: ATR DOWNWARD PRICE GAP
# ==========================================

print("\nTEST 58: ATR DOWNWARD PRICE GAP")

# Create OHLC data containing a downward price gap.
test_data = pd.DataFrame({
    "High": [12.0, 9.0],
    "Low": [10.0, 7.0],
    "Close": [10.0, 8.0]
})

# Calculate ATR using a period of 2.
atr = calculate_atr(
    test_data,
    period=2
)

# First True Range = 12 - 10 = 2.
# Second True Range = 10 - 7 = 3.
# Initial ATR = (2 + 3) / 2 = 2.5.

expected_atr = 2.5

# Confirm that ATR accounts for the downward price gap.
assert np.isclose(
    atr.iloc[1],
    expected_atr
), "ATR failed to account for the downward price gap."

print("TEST 58 PASSED: ATR correctly accounts for downward price gaps.")


# ==========================================
# TEST 59: ATR PERIOD OF ONE
# ==========================================

print("\nTEST 59: ATR PERIOD OF ONE")

# Create OHLC data with different True Range values.
test_data = pd.DataFrame({
    "High": [12.0, 15.0, 14.0],
    "Low": [10.0, 13.0, 12.0],
    "Close": [11.0, 14.0, 13.0]
})

# Calculate ATR using a period of 1.
atr = calculate_atr(
    test_data,
    period=1
)

# Expected True Range values:
# Candle 1: 2
# Candle 2: 4
# Candle 3: 2

expected_atr = [2.0, 4.0, 2.0]

# Confirm that ATR equals True Range for every candle.
assert np.allclose(
    atr.to_numpy(),
    expected_atr
), "ATR period of 1 produced incorrect values."

print("TEST 59 PASSED: ATR period of 1 works correctly.")


# ==========================================
# TEST 60: ZERO-VOLATILITY MARKET CONDITIONS
# ==========================================

print("\nTEST 60: ZERO-VOLATILITY MARKET CONDITIONS")

# Create OHLC data with no price movement.
test_data = pd.DataFrame({
    "High": [10.0, 10.0, 10.0, 10.0],
    "Low": [10.0, 10.0, 10.0, 10.0],
    "Close": [10.0, 10.0, 10.0, 10.0]
})

# Calculate ATR using a period of 2.
atr = calculate_atr(
    test_data,
    period=2
)

# Confirm that the initial ATR value is zero.
assert np.isclose(
    atr.iloc[1],
    0.0
), "ATR should be zero when there is no price movement."

# Confirm that subsequent ATR values remain zero.
assert np.allclose(
    atr.iloc[1:].to_numpy(),
    0.0
), "ATR should remain zero during zero-volatility conditions."

print("TEST 60 PASSED: Zero-volatility market conditions handled correctly.")


# ==========================================
# TEST 61: INITIAL WILDER RSI CALCULATION
# ==========================================

print("\nTEST 61: INITIAL WILDER RSI CALCULATION")

prices = pd.Series([100, 102, 101, 104, 102, 103])

# Use a period of 3 to make the calculation easy to verify.
rsi = calculate_rsi(prices, period=3)

# First three price changes:
# Gains: 2, 0, 3
# Losses: 0, 1, 0
#
# Average gain = 5 / 3
# Average loss = 1 / 3
# RSI = 83.3333...

expected_rsi = 83.3333333333

assert np.isclose(
    rsi.iloc[3],
    expected_rsi,
    atol=0.0001
), "Initial Wilder RSI calculation is incorrect."

print("TEST 61 PASSED: Initial RSI uses simple average gains and losses.")


# ==========================================
# TEST 62: SUBSEQUENT WILDER RSI SMOOTHING
# ==========================================

print("\nTEST 62: SUBSEQUENT WILDER RSI SMOOTHING")

prices = pd.Series([100, 102, 101, 104, 102, 103])

rsi = calculate_rsi(prices, period=3)

# Expected RSI values after applying Wilder's smoothing.
expected_rsi_index_4 = 55.5555555556
expected_rsi_index_5 = 64.4444444444

assert np.isclose(
    rsi.iloc[4],
    expected_rsi_index_4,
    atol=0.0001
), "Wilder RSI smoothing at index 4 is incorrect."

assert np.isclose(
    rsi.iloc[5],
    expected_rsi_index_5,
    atol=0.0001
), "Wilder RSI smoothing at index 5 is incorrect."

print("TEST 62 PASSED: Subsequent RSI values use Wilder's smoothing.")