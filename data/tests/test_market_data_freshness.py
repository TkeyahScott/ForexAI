
# ==========================================
# FOREXAI: MARKET DATA FRESHNESS TEST
# ==========================================

import time
import MetaTrader5 as mt5

from datetime import datetime, timezone

# Import the central UTC timestamp conversion function.
from data.market_data import convert_broker_timestamps_to_utc


# ForexAI initial watchlist.
WATCHLIST = [
    "EURUSD",
    "USDJPY",
    "GBPUSD",
    "EURJPY",
    "GBPJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF"
]


print("\n=== FOREXAI: MARKET DATA FRESHNESS TEST ===\n")

try:

    # Connect to MetaTrader 5.
    if not mt5.initialize():
        raise RuntimeError(
            f"MT5 connection failed: {mt5.last_error()}"
        )


    # Inspect every currency pair.
    for symbol in WATCHLIST:

        print(f"\nCURRENCY PAIR: {symbol}")
        print("--------------------------------")

        # Make the symbol available in Market Watch.
        if not mt5.symbol_select(symbol, True):
            print("Symbol selection failed.")
            continue

        # Retrieve the latest live tick.
        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print("Live tick unavailable.")
            continue

        # Retrieve the latest completed M15 candle.
        rates = mt5.copy_rates_from_pos(
            symbol,
            mt5.TIMEFRAME_M15,
            1,
            1
        )

        if rates is None or len(rates) == 0:
            print("Historical M15 candle unavailable.")
            continue

        # Capture computer UTC after retrieving market data.
        computer_epoch = time.time()

        # Convert the tick timestamp into UTC.
        raw_tick_epoch = (
            tick.time_msc / 1000
            if tick.time_msc
            else float(tick.time)
        )

        # MT5 tick timestamps are already Unix UTC timestamps.
        # Do not subtract the broker's timezone offset.
        tick_age = computer_epoch - raw_tick_epoch

        # Convert the MT5 candle timestamp directly into UTC.
        candle_df = convert_broker_timestamps_to_utc(
           [rates[0]["time"]]
        )

        candle_time = candle_df.iloc[0]

        candle_age_minutes = (
            computer_epoch - candle_time.timestamp()
        ) / 60

        # Display results.
        print("Latest M15 candle UTC:", candle_time)

        print(
            f"Completed candle age: "
            f"{candle_age_minutes:.2f} minutes"
        )

        print(f"Live tick age: {tick_age:.2f} seconds")

        # Classify the latest tick.
        if tick_age > 300:
            print("LIVE TICK STATUS: STALE")
        elif tick_age < -10:
            print("LIVE TICK STATUS: FUTURE TIMESTAMP")
        else:
            print("LIVE TICK STATUS: RECENT")

        # Classify the latest completed candle.
        if candle_age_minutes > 30:
            print("CANDLE STATUS: STALE")
        elif candle_age_minutes < 0:
            print("CANDLE STATUS: FUTURE TIMESTAMP")
        else:
            print("CANDLE STATUS: RECENT")

        print("\n=== FRESHNESS TEST FINISHED ===")

finally:

    # Close the MT5 connection.
    mt5.shutdown()
