
# Import the MetaTrader 5 package.
import MetaTrader5 as mt5


# ==========================================
# FOREXAI: MT5 VERSION TEST
# ==========================================

print("\n=== FOREXAI: MT5 VERSION TEST ===\n")

# Display the installed Python package version.
print("Python package version:", mt5.__version__)

# Connect to the running MT5 terminal.
if not mt5.initialize():

    print("MT5 connection failed:", mt5.last_error())

else:

    try:
        # Retrieve information about the connected terminal.
        terminal = mt5.terminal_info()

        if terminal is not None:

            print("\nTERMINAL INFORMATION")
            print("--------------------------------")

            print("Terminal version:", terminal.build)
            print("Terminal name:", terminal.name)
            print("Terminal connected:", terminal.connected)

        else:

            print("Could not retrieve terminal information.")

        # Retrieve account/server information.
        account = mt5.account_info()

        if account is not None:

            print("\nACCOUNT INFORMATION")
            print("--------------------------------")

            print("Broker server:", account.server)
            print("Account currency:", account.currency)

    finally:

        # Close the MT5 connection.
        mt5.shutdown()

print("\n=== VERSION TEST FINISHED ===")
