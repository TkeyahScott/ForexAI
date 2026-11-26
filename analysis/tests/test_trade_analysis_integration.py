# ==========================================
# FOREXAI: TRADE ANALYSIS INTEGRATION TEST
# ==========================================

# Tests the complete H4, H1 and M15 strategy
# using processed MT5 market data.

from data.market_data import get_watchlist_market_data
from analysis.indicator_pipeline import process_market_data
from analysis.trade_analyzer import analyze_market

# ==========================================
# EXPECTED MARKET SYMBOLS
# ==========================================

EXPECTED_SYMBOLS = [
    "EURUSD",
    "USDJPY",
    "GBPUSD",
    "EURJPY",
    "GBPJPY",
    "AUDUSD",
    "USDCAD",
    "USDCHF"
]


# ==========================================
# REQUIRED TIMEFRAMES
# ==========================================

REQUIRED_TIMEFRAMES = [
    "H4",
    "H1",
    "M15"
]

# ==========================================
# LIVE TRADE ANALYSIS INTEGRATION TEST
# ==========================================

def test_live_trade_analysis():
    
    # Track the number of successfully analyzed pairs.
    analyzed_symbols = 0
    skipped_symbols = 0

    print("\nStarting ForexAI trade analysis integration test...")

    # --------------------------------------
    # STEP 1: Retrieve MT5 market data
    # --------------------------------------

    print("\nRetrieving MT5 market data...")

    market_data = get_watchlist_market_data()

    if market_data is None:
        raise RuntimeError(
            "Market data retrieval failed. "
            "Check that MT5 is open and connected."
        )

    print("Market data retrieved successfully.")

    # --------------------------------------
    # STEP 2: Calculate technical indicators
    # --------------------------------------

    print("\nProcessing technical indicators...")

    processed_data = process_market_data(market_data)

    if processed_data is None:
        raise RuntimeError(
            "The indicator pipeline returned no processed data."
        )

    print("Indicator processing completed.")

    # --------------------------------------
    # STEP 3: Analyze each currency pair
    # --------------------------------------

    print("\nGenerating multi-timeframe trade analysis...")

    for symbol in EXPECTED_SYMBOLS:

        if symbol not in processed_data:
            print(f"SKIPPED: {symbol} - market data unavailable.")
            skipped_symbols += 1
            continue

        symbol_data = processed_data[symbol]

        # Check that all three required timeframes exist.
        if not all(
            symbol_data.get(timeframe) is not None
            for timeframe in REQUIRED_TIMEFRAMES
        ):
            print(f"SKIPPED: {symbol} - incomplete timeframe data.")
            skipped_symbols += 1
            continue

        # Retrieve the processed H4, H1 and M15 datasets.
        h4_data = symbol_data["H4"]
        h1_data = symbol_data["H1"]
        m15_data = symbol_data["M15"]

        # Run the complete multi-timeframe analyzer.
        result = analyze_market(
            h4_data,
            h1_data,
            m15_data
        )

        # Display the analysis results.
        print(f"\n=== {symbol} ANALYSIS ===")
        print(f"H4 trend: {result['h4_trend']}")
        print(f"H1 confirmation: {result['h1_trend']}")
        print(f"M15 entry signal: {result['entry_signal']}")
        analyzed_symbols += 1

    # At least one currency pair must be analyzed.
    if analyzed_symbols == 0:
        raise RuntimeError(
            "No currency pairs were successfully analyzed."
        )

    # --------------------------------------
    # STEP 4: Display analysis summary
    # --------------------------------------

    print("\n==========================================")
    print("TRADE ANALYSIS INTEGRATION SUMMARY")
    print("==========================================")

    print(f"Successfully analyzed: {analyzed_symbols}")
    print(f"Skipped symbols: {skipped_symbols}")

    print("\nTRADE ANALYSIS INTEGRATION TEST COMPLETED.")

if __name__ == "__main__":

    try:
        test_live_trade_analysis()

    except Exception as error:

        print("\nLIVE TRADE ANALYSIS INTEGRATION TEST FAILED.")
        print(f"Reason: {error}")

        # Preserve the error details for troubleshooting.

        raise