
# ==========================================
# FOREXAI: MARKET CONFIGURATION TEST
# ==========================================

# Import the offset directly from central configuration.
from config.market_settings import BROKER_UTC_OFFSET_SECONDS

# Import the market data conversion function.
from data.market_data import convert_broker_timestamps_to_utc

print("\n=== FOREXAI: MARKET CONFIGURATION TEST ===\n")

print("CENTRAL BROKER CONFIGURATION")
print("--------------------------------")
print("Broker UTC offset:", BROKER_UTC_OFFSET_SECONDS, "seconds")
print("Broker UTC offset:", BROKER_UTC_OFFSET_SECONDS / 3600, "hours")

# Test a known timestamp.
test_timestamp = 1794369600

converted_timestamp = convert_broker_timestamps_to_utc(test_timestamp)

print("\nTIMESTAMP CONVERSION")
print("--------------------------------")
print("Original timestamp:", test_timestamp)
print("Converted UTC timestamp:", converted_timestamp)

print("\n=== TEST FINISHED ===")
