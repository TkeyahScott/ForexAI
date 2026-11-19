import pandas as pd
from analysis.technical_indicators import calculate_ema, calculate_rsi
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
