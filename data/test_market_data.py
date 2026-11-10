# Import the MT5 library so we can access its timeframe constants.
import MetaTrader5 as mt5

# Import our historical market data retrieval function.
from data.market_data import get_historical_data


# ==========================================
# FOREXAI: MARKET DATA ENGINE TEST
# ==========================================

print("\n=== FOREXAI: MARKET DATA TEST ===\n")

# Specify the currency pair we want to test.
symbol = "EURUSD"

# Specify the timeframe: 15-minute candles.
timeframe = mt5.TIMEFRAME_M15

# Request the latest 100 historical candles.
number_of_candles = 100


# Retrieve the historical market data.
market_data = get_historical_data(
    symbol,
    timeframe,
    number_of_candles
)


# Check whether the retrieval was successful.
if market_data is not None:

    print("\nHistorical market data retrieved successfully!")

    # Display the number of candles received.
    print("\nTotal candles:", len(market_data))

    # Display the five most recent candles.
    print("\nLatest five candles:")

    print(
        market_data[
            ["time", "open", "high", "low", "close", "tick_volume"]
        ].tail(5).to_string(index=False)
    )

    # Display the structure of the retrieved data.
    print("\nData information:")

    # Display the DataFrame structure and data types.
    # info() prints its results directly, so we don't wrap it in print().
    market_data.info()
    
    print("\nFOREXAI MARKET DATA TEST PASSED!")

else:

    # Display an error if historical data retrieval failed.
    print("\nFOREXAI MARKET DATA TEST FAILED!")
