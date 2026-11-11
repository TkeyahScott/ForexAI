# Ensure the requested pair names are the same. 
# Import MetaTrader 5 so Python can communicate with the MT5 terminal.
import MetaTrader5 as mt5


# ==========================================
# FOREXAI: MT5 SYMBOL DISCOVERY
# ==========================================

# These are the eight currency pairs in our initial ForexAI watchlist.
requested_pairs = [
    "EURUSD",
    "USDJPY",
    "GBPUSD",
    "EURJPY",
    "GBPJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF"
]


print("\n=== FOREXAI: SYMBOL DISCOVERY ===\n")


# Initialise the connection to the running MT5 desktop terminal.
if not mt5.initialize():

    print("MT5 connection failed:", mt5.last_error())

else:

    try:
        # Retrieve the complete list of symbols available in MT5.
        available_symbols = mt5.symbols_get()

        # Check whether MT5 returned a symbol list.
        if available_symbols is None:

            print("Could not retrieve the MT5 symbol list.")
            print("MT5 error:", mt5.last_error())

        else:

            print("MT5 symbol list retrieved successfully.\n")

            # Check each requested currency pair against the broker's symbols.
            for pair in requested_pairs:

                print(f"\nSearching for {pair}...")

                # Find symbols whose names begin with the requested pair.
                matches = [
                    symbol.name
                    for symbol in available_symbols
                    if symbol.name.upper().startswith(pair)
                ]

                # Display the matching broker symbol names.
                if matches:

                    for match in matches:
                        print("  Found:", match)

                else:

                    print("  No matching symbol found.")

    finally:

        # Close the MT5 connection after the discovery process finishes.
        mt5.shutdown()

print("\n=== SYMBOL DISCOVERY FINISHED ===")
