ForexAI
KeyS Devs
23/11/2026


ForexAI is a Python-based Forex market analysis and trading-system project that connects to MetaTrader 5 (MT5) to retrieve, organise and analyse market data.

The project is being developed in stages. Its intended direction is a semi-automated trading assistant: it will analyse market conditions and present potential trade opportunities for the user to review and approve. It is not intended to place trades without explicit user approval.

Development status: Phase 3 completed — Technical Indicators and Market Data Analysis Pipeline. Phase 4 — Trade Analysis and Signal Generation — is the next development stage.

Important: ForexAI is currently a development/demo project. Although market data retrieval and technical-indicator processing have been implemented and tested, trade analysis and signal generation are still under development. The system does not currently provide validated trading signals or place trades. No profitability is guaranteed. Do not connect the project to a live account or use real funds during development and testing.

Project goals

The longer-term project is intended to include:

Market data collection from MetaTrader 5.

Analysis across a selected Forex watchlist and multiple chart timeframes.

Technical indicators and independently testable strategy modules.

Rule-based market analysis and potential trade-signal generation.

Risk-management checks before a trade idea can be presented.

A dashboard for reviewing analysis and proposed trades.

Explicit user approval before any trade execution.

Performance tracking, backtesting and strategy evaluation.

These are project goals, not claims that all features are already implemented.

Current development status

Completed

Created the Python project structure.

Set up a Python virtual environment.

Installed and tested the core Python libraries.

Connected Python to the MetaTrader 5 desktop terminal using a demo account.

Retrieved historical EURUSD candlestick data.

Implemented market-data retrieval for the initial eight-pair watchlist.

Implemented historical candle retrieval across M15, H1 and H4 timeframes.

Excluded the currently forming candle from completed-candle analysis.

Implemented broker timestamp conversion using the agreed EBT → UTC → TT approach.

Standardised UTC as the internal timestamp reference for data processing.

Added Trinidad and Tobago time conversion for user-facing timestamps.

Added seasonal European broker-time handling for the current MetaQuotes-Demo configuration.

Implemented EMA20 and EMA50 calculations.

Implemented RSI14 calculations.

Implemented ATR14 calculations.

Created a technical-indicator pipeline to enrich market datasets with the calculated indicators.

Added unit and integration tests for the technical indicators and processing pipeline.

Successfully tested the live indicator pipeline across all 24 symbol/timeframe datasets (8 currency pairs × 3 timeframes).

Verified that all 24 datasets were successfully processed with all four technical indicators.

Committed and pushed the completed timestamp-conversion and indicator-pipeline updates to GitHub.

In progress / planned

Develop the multi-timeframe trade-analysis engine.

Implement H4 trend identification.

Implement H1 trend and momentum confirmation.

Develop M15 pullback and reclaim entry conditions.

Implement BUY, SELL and NO TRADE signal decisions.

Calculate potential entry, stop-loss and take-profit levels.

Implement risk/reward assessment and risk-management validation.

Add independent strategy testing and validation.

Implement historical backtesting and performance evaluation.

Build the analysis and approval dashboard.

Add demo-only trade execution after the analysis and risk-management components have been tested.

Add performance tracking and reporting.

Initial Forex watchlist

The initial watchlist contains these eight currency pairs:

EURUSD

USDJPY

GBPUSD

EURJPY

GBPJPY

AUDUSD

USDCAD

USDCHF

The broker may use a suffix or a different symbol format. ForexAI discovers and verifies the exact symbol names in MT5 rather than assuming that the names above are available exactly as written.

Market data and timeframes

ForexAI currently retrieves completed historical candlestick data across three timeframes:

M15: 15-minute candles.

H1: 1-hour candles.

H4: 4-hour candles.

This provides 24 possible market datasets across the eight currency pairs.

The currently forming candle is excluded from the completed-candle analysis so that indicators and future strategy decisions are based on completed price data.

Technical indicators

The technical-indicator pipeline currently calculates four indicators:

EMA20: 20-period Exponential Moving Average.

EMA50: 50-period Exponential Moving Average.

RSI14: 14-period Relative Strength Index.

ATR14: 14-period Average True Range.

The indicators are calculated for each available symbol and timeframe dataset.

The pipeline preserves the original market data while adding the indicator values for subsequent analysis.

Timezone handling

ForexAI uses a consistent timestamp-conversion process:

EBT → UTC → TT

EBT (European Broker Time): Used to interpret the broker's server-time timestamps for the current MetaQuotes-Demo configuration.

UTC: The internal standard for data processing, timestamp alignment, indicator calculations and database storage.

TT (Trinidad and Tobago Time): Used for user-facing information, including displayed timestamps and reports.

European broker time changes seasonally between UTC+2 and UTC+3. The conversion uses European timezone rules rather than a permanently fixed offset.

Trinidad and Tobago does not observe daylight saving time. User-facing timestamps are intended to use Trinidad local time with a 12-hour clock and AM/PM format.

The current broker-time interpretation must be verified before connecting ForexAI to a different broker or server configuration.

Initial trading strategy

The first planned strategy uses a multi-timeframe analysis approach:

H4 — Main trend: Identify the broader bullish or bearish market direction using EMA20 and EMA50, with price confirmation.

H1 — Trend and momentum confirmation: Check whether the shorter-term trend and RSI14 agree with the H4 direction.

M15 — Entry conditions: Identify a potential pullback and reclaim entry, with RSI confirmation.

Risk assessment: Use ATR14 to help assess stop-loss distance and evaluate the potential risk/reward.

The intended signal decisions are:

BUY: Conditions support a potential buy opportunity.

SELL: Conditions support a potential sell opportunity.

NO TRADE: Conditions are conflicting, incomplete or do not satisfy the strategy rules.

This is the initial Strategy 1.0 design. The rules will be implemented, tested and refined. Additional indicators, strategies and price-action techniques may be incorporated as development progresses.

The strategy has not yet been validated through backtesting or demo forward-testing. Its rules should not be interpreted as proven profitable.

Technology

Python — application and analysis logic

MetaTrader 5 Python integration — terminal connection and market data

Pandas — tabular market data and timestamp processing

NumPy — numerical operations

Streamlit — planned dashboard

Matplotlib — planned charts and visual analysis

SQLite — planned local data/performance storage

The installed dependencies are listed in requirements.txt.

Project structure

ForexAI/
├── analysis/
│   ├── tests/
│   │   ├── test_indicator_integration.py
│   │   ├── test_indicator_pipeline.py
│   │   └── test_technical_indicators.py
│   ├── indicator_pipeline.py
│   └── technical_indicators.py
├── config/                       # Future application configuration
├── dashboard/                    # Future dashboard
├── data/
│   ├── market_data.py            # Historical candle retrieval and timestamp conversion
│   ├── test_market_configuration.py
│   ├── test_market_data.py
│   └── test_multi_timeframe.py
├── risk_management/               # Future risk checks
├── trading_engine/
│   ├── mt5_connection.py         # MT5 connection diagnostic
│   └── __init__.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt

Some folders are currently placeholders for planned components. The project structure will expand as additional features are developed.

Requirements

Windows (the current development environment)

Python installed

MetaTrader 5 desktop terminal installed and running

Access to an MT5 demo account for development testing

VS Code or another Python editor (recommended)

Setup

1. Clone the repository

If you are setting up the project from GitHub:

git clone <YOUR-REPOSITORY-URL>
cd ForexAI

Replace <YOUR-REPOSITORY-URL> with the actual repository URL.

If you already have the project folder on your computer, open that folder in VS Code and skip the clone step.

2. Create and activate a virtual environment

Run these commands from the project root in PowerShell:

python -m venv .venv

If PowerShell blocks activation scripts, allow script execution for the current terminal session and activate the environment:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1

When activated, the terminal prompt should show (.venv).

3. Install dependencies

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

4. Start MetaTrader 5

Open the MT5 desktop terminal and sign in to the demo account. Keep the terminal running while testing the Python connection.

Running the current tests

Run commands from the ForexAI project root, with the virtual environment activated.

Test the MT5 connection

python .\trading_engine\mt5_connection.py

This diagnostic checks whether Python can connect to the running MT5 terminal and retrieve a sample quote and recent candles.

Test historical market-data retrieval

python -m data.test_market_data

The market-data test checks historical candle retrieval from the connected MT5 terminal.

Test market configuration and timestamp conversion

python -m data.test_market_configuration

This test checks the broker timestamp conversion into UTC.

Test multi-timeframe market data

python -m data.test_multi_timeframe

This test checks the retrieval and processing of the eight currency pairs across M15, H1 and H4.

Test technical indicators

python -m analysis.tests.test_technical_indicators

This test checks the individual EMA, RSI and ATR calculations.

Test the indicator pipeline

python -m analysis.tests.test_indicator_pipeline

This test checks that the technical-indicator pipeline correctly enriches market-data datasets.

Test live indicator integration

python -m analysis.tests.test_indicator_integration

This integration test checks the retrieval of live market datasets and verifies that the four technical indicators are successfully added to each available dataset.

Market-data notes

Candle timestamps are converted to UTC for consistent internal processing.

User-facing timestamps are converted to Trinidad and Tobago local time.

The current historical-data function starts from candle position 1, which skips the candle that is still forming.

MT5 can return fewer historical candles than requested if the terminal does not have enough history downloaded or available.

Tick volume represents the number of price updates/ticks recorded for a candle; it is not necessarily the number of transactions.

Broker symbol names, timestamp behaviour and available history must be checked in the connected MT5 terminal.

The current broker-time conversion is configured around the observed MetaQuotes-Demo server behaviour and should be verified before use with another broker.

Safety and development principles

Development and initial testing should use an MT5 demo account only.

The system must not place a trade without explicit user approval.

A proposed trade must not bypass risk-management checks.

Stop-loss and position-sizing rules must be validated before any execution feature is enabled.

Strategy performance must be evaluated with historical testing and demo forward-testing, including transaction costs and slippage.

Backtested or demo results do not guarantee future performance.

An AI language model may help explain results, but must not invent market signals or override deterministic risk controls.

Version control

The project uses Git. The primary branch is main.

Useful commands:

git status
git add .
git commit -m "Describe your changes"
git log -1 --oneline

The .gitignore file excludes the virtual environment, Python cache files, local environment files and editor settings. Do not commit passwords, API keys, account credentials or other secrets.

Disclaimer

Forex trading involves substantial risk and may not be suitable for everyone. ForexAI is an educational software-development project, not financial advice or a guarantee of returns. Always test thoroughly in a demo environment before considering any live use.