import MetaTrader5 as mt5
import pandas as pd


def connect_to_mt5():
    """Connect ForexAI to the running MT5 desktop terminal."""

    print("\n=== FOREXAI: MT5 CONNECTION TEST ===\n")

    if not mt5.initialize():
        print("Connection failed!")
        print("Error:", mt5.last_error())
        return

    try:
        terminal = mt5.terminal_info()
        account = mt5.account_info()

        if terminal is None or account is None:
            print("Could not retrieve terminal or account information.")
            return

        if not terminal.connected:
            print("MT5 terminal is not connected to the broker.")
            return

        print("MT5 connection successful!")
        print("Broker server:", account.server)
        print("Account currency:", account.currency)
        print("Terminal connected:", terminal.connected)

        # Find EURUSD, including broker-specific suffixes.
        symbols = mt5.symbols_get()

        matching_symbols = [
            symbol.name
            for symbol in (symbols or ())
            if symbol.name.startswith("EURUSD")
        ]

        if not matching_symbols:
            print("\nEURUSD was not found.")
            print("Check whether EURUSD is available in Market Watch.")
            return

        symbol = (
            "EURUSD"
            if "EURUSD" in matching_symbols
            else matching_symbols[0]
        )

        if not mt5.symbol_select(symbol, True):
            print("Could not select:", symbol)
            return

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print("Could not retrieve current market price.")
            return

        print(f"\nMarket data: {symbol}")
        print("Bid:", tick.bid)
        print("Ask:", tick.ask)

        # Retrieve the five latest 15-minute candles.
        rates = mt5.copy_rates_from_pos(
            symbol,
            mt5.TIMEFRAME_M15,
            0,
            5
        )

        if rates is None or len(rates) == 0:
            print("Could not retrieve historical price data.")
            print("Error:", mt5.last_error())
            return

        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")

        print("\nLatest five 15-minute candles:")
        print(
            df[
                ["time", "open", "high", "low", "close", "tick_volume"]
            ].to_string(index=False)
        )

        print("\nFOREXAI CONNECTION TEST PASSED!")

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    connect_to_mt5()
