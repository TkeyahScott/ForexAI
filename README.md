ForexAI
KeyS Devs
10/11/2026


ForexAI is a Python-based Forex market analysis and trading-system project that connects to MetaTrader 5 (MT5) to retrieve and organise market data.

The project is being developed in stages. Its intended direction is a semi-automated trading assistant: it will analyse market conditions and present potential trade opportunities for the user to review and approve. It is not intended to place trades without explicit user approval.
Development status: Early development — Phase 2 (Market Data Engine).

Important: ForexAI is currently a development/demo project. The market-data tools do not place trades. No profitability is guaranteed. Do not connect the project to a live account or use real funds during development and testing.

Project goals
The longer-term project is intended to include:
- Market data collection from MetaTrader 5.
- Analysis across a selected Forex watchlist and multiple chart timeframes.
- Independently testable strategy modules.
- Risk-management checks before a trade idea can be presented.
- A dashboard for reviewing analysis and proposed trades.
- Explicit user approval before any trade execution.
- Performance tracking and strategy evaluation.
These are project goals, not claims that all features are already implemented.
Current development status
Completed
- [x] Created the Python project structure.
- [x] Set up a Python virtual environment.
- [x] Installed and tested the core Python libraries.
- [x] Connected Python to the MetaTrader 5 desktop terminal using a demo account.
- [x] Retrieved historical EURUSD candlestick data.
- [x] Converted candle timestamps to UTC-aware datetime values.
- [x] Excluded the currently forming candle from the historical-data request.
- [x] Added a basic market-data retrieval test.
- [x] Initialised a local Git repository and created the first commit.
In progress / planned
- [ ] Discover the broker's exact symbol names for the Forex watchlist.
- [ ] Retrieve data for all eight initial currency pairs.
- [ ] Retrieve data on M15, H1 and H4 timeframes.
- [ ] Add market-data validation (missing values, duplicates, candle consistency and gaps).
- [ ] Improve MT5 connection management for repeated data requests.
- [ ] Build and test strategy modules independently.
- [ ] Add risk-management rules and validation.
- [ ] Build the analysis and approval dashboard.
- [ ] Add demo-only execution after the preceding components have been tested.
- [ ] Add performance tracking and backtesting.
Initial Forex watchlist
The planned initial watchlist contains these eight currency pairs:
1. EURUSD
2. USDJPY
3. GBPUSD
4. EURJPY
5. GBPJPY
6. AUDUSD
7. USDCAD
8. USDCHF
The broker may use a suffix or a different symbol format. ForexAI must discover and verify the exact symbol names in MT5 rather than assume that the names above are available exactly as written.
Technology
- Python — application and analysis logic
- MetaTrader 5 Python integration — terminal connection and market data
- Pandas — tabular market data
- NumPy — numerical operations
- Streamlit — planned dashboard
- Matplotlib — planned charts and visual analysis
- SQLite — planned local data/performance storage
The installed dependencies are listed in requirements.txt.
Project structure
ForexAI/
├── analysis/                 # Future market and strategy analysis modules
├── config/                   # Future application configuration
├── dashboard/                # Future dashboard
├── data/
│   ├── market_data.py        # Historical candle retrieval from MT5
│   └── test_market_data.py   # Market-data retrieval test
├── risk_management/          # Future risk checks
├── trading_engine/
│   └── mt5_connection.py     # MT5 connection diagnostic
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
Some folders are currently placeholders for planned components.
Requirements
- Windows (the current development environment)
- Python installed
- MetaTrader 5 desktop terminal installed and running
- Access to an MT5 demo account for development testing
- VS Code or another Python editor (recommended)
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
The current test requests 100 completed EURUSD M15 candles and displays a sample of the returned data.
Market-data notes
- Candle timestamps are kept in UTC so data from different markets and timeframes can be compared consistently.
- The current historical-data function starts from candle position 1, which skips the candle that is still forming.
- MT5 can return fewer historical candles than requested if the terminal does not have enough history downloaded or available.
- Tick volume represents the number of price updates/ticks recorded for a candle; it is not necessarily the number of transactions.
- Broker symbol names and available history must be checked in the connected MT5 terminal.
Safety and development principles
- Development and initial testing should use an MT5 demo account only.
- The system must not place a trade without explicit user approval.
- A proposed trade must not bypass risk-management checks.
- Stop-loss and position-sizing rules must be validated before any execution feature is enabled.
- Strategy performance must be evaluated with historical testing and demo forward-testing, including transaction costs and slippage.
- Backtested or demo results do not guarantee future performance.
- An AI language model may help explain results, but must not invent market signals or override deterministic risk controls.
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