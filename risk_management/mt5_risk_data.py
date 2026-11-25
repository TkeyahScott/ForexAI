# ==========================================
# FOREXAI: MT5 RISK DATA
# ==========================================

# Handles:
# - Retrieving account balance and currency.
# - Retrieving symbol tick specifications.
# - Retrieving broker volume restrictions.
#
# This module is READ-ONLY.
# It does not place or modify trades.

import MetaTrader5 as mt5


def get_mt5_risk_data(symbol):
    """
    Retrieve account and symbol information
    required for position sizing.

    MT5 must already be initialized.

    Args:
        symbol (str): Forex symbol, e.g. EURUSD.

    Returns:
        dict: Account and broker risk specifications.

    Raises:
        RuntimeError: If MT5 information cannot be retrieved.
        ValueError: If required specifications are invalid.
    """

    # Retrieve the connected trading account.
    account = mt5.account_info()

    if account is None:
        raise RuntimeError(
            f"Unable to retrieve MT5 account information: {mt5.last_error()}"
        )

    # Retrieve the requested symbol specifications.
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise RuntimeError(
            f"Unable to retrieve specifications for {symbol}: "
            f"{mt5.last_error()}"
        )

    # Use the loss-side tick value for risk calculations.
    tick_value = symbol_info.trade_tick_value_loss

    # Collect the required values.
    risk_data = {
        "symbol": symbol,
        "account_balance": account.balance,
        "account_currency": account.currency,
        "tick_size": symbol_info.trade_tick_size,
        "tick_value": tick_value,
        "volume_min": symbol_info.volume_min,
        "volume_max": symbol_info.volume_max,
        "volume_step": symbol_info.volume_step
    }

    # Ensure all required numerical specifications are positive.
    for field, value in risk_data.items():
        if field not in ("symbol", "account_currency"):
            if value is None or value <= 0:
                raise ValueError(
                    f"Invalid MT5 risk specification: {field}={value}"
                )

    return risk_data