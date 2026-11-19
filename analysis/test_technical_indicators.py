import pandas as pd

from analysis.technical_indicators import calculate_ema


# ==========================================
# FOREXAI: TECHNICAL INDICATOR TESTS
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