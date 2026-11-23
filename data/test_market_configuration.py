
# ==========================================
# FOREXAI: UTC TIMESTAMP CONVERSION TEST
# ==========================================

import pandas as pd

from data.market_data import convert_broker_timestamps_to_utc


print("\n=== FOREXAI: UTC TIMESTAMP CONVERSION TEST ===\n")


# ==========================================
# TEST A KNOWN UNIX TIMESTAMP
# ==========================================

# This Unix timestamp represents:
# 11 November 2026 at 04:00:00 UTC.
test_timestamp = 1794369600

# The conversion function accepts a list or Pandas Series.
converted_timestamp = convert_broker_timestamps_to_utc(
    [test_timestamp]
)

# Extract the converted timestamp from the Series.
result = converted_timestamp.iloc[0]

# Define the expected UTC result.
expected_timestamp = pd.Timestamp(
    "2026-11-11 02:00:00",
    tz="UTC"
)


# ==========================================
# VALIDATION
# ==========================================

print("TIMESTAMP CONVERSION")
print("--------------------------------")
print("Original Unix timestamp:", test_timestamp)
print("Converted UTC timestamp:", result)
print("Expected UTC timestamp:", expected_timestamp)

# Confirm that the timestamp was converted correctly.
assert result == expected_timestamp, (
    "Timestamp conversion produced an incorrect result."
)

# Confirm that the result is timezone-aware UTC.
assert str(result.tz) == "UTC", (
    "Timestamp is not UTC-aware."
)

print("\nUTC CONVERSION TEST: PASSED")

print("\n=== TEST FINISHED ===")
