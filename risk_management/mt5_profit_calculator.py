
# ==========================================
# FOREXAI: MT5 PROFIT CALCULATOR
# ==========================================

# Handles:
# - Calculating projected trade profit/loss through MT5.
# - Verifying monetary loss per lot.
#
# This module is READ-ONLY.
# It does not place trades.

import math
import MetaTrader5 as mt5

def calculate_mt5_loss_per_lot(
    symbol,
    direction,
    entry_price,
    stop_loss
):
    """
    Calculate the projected monetary loss for one lot
    if the trade reaches its stop loss.

    MT5 must already be initialized.

    Args:
        symbol (str): Forex symbol, e.g. EURUSD.
        direction (str): BUY or SELL.
        entry_price (float): Proposed entry price.
        stop_loss (float): Proposed stop-loss price.

    Returns:
        dict: Projected loss per lot in account currency.
    """

    # Validate direction.
    direction = str(direction).upper()

    if direction not in ("BUY", "SELL"):
        raise ValueError("Direction must be BUY or SELL.")

    # Convert prices to numerical values.
    try:
        entry_price = float(entry_price)
        stop_loss = float(stop_loss)
    except (TypeError, ValueError):
        raise ValueError("Entry and stop-loss prices must be numeric.")

    # Reject invalid numerical values.
    if not math.isfinite(entry_price) or not math.isfinite(stop_loss):
        raise ValueError("Prices must be finite.")

    if entry_price <= 0 or stop_loss <= 0:
        raise ValueError("Prices must be positive.")

    # Verify stop-loss placement.
    if direction == "BUY" and stop_loss >= entry_price:
        raise ValueError("BUY stop loss must be below entry price.")

    if direction == "SELL" and stop_loss <= entry_price:
        raise ValueError("SELL stop loss must be above entry price.")

    # Confirm MT5 account connection.
    account = mt5.account_info()

    if account is None:
        raise RuntimeError(
            f"Unable to retrieve MT5 account: {mt5.last_error()}"
        )

    # Ensure the symbol is selected in Market Watch.
    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(
            f"Unable to select {symbol}: {mt5.last_error()}"
        )

    # Select the MT5 order direction.
    order_type = (
        mt5.ORDER_TYPE_BUY
        if direction == "BUY"
        else mt5.ORDER_TYPE_SELL
    )

    # Ask MT5 to calculate the projected result for one lot.
    projected_profit = mt5.order_calc_profit(
        order_type,
        symbol,
        1.0,
        entry_price,
        stop_loss
    )

    if projected_profit is None:
        raise RuntimeError(
            f"MT5 profit calculation failed: {mt5.last_error()}"
        )

    projected_profit = float(projected_profit)

    if not math.isfinite(projected_profit):
        raise ValueError("MT5 returned an invalid profit calculation.")

    if projected_profit >= 0:
        raise ValueError(
            "Stop-loss calculation did not produce a monetary loss."
        )

    return {
        "symbol": symbol,
        "direction": direction,
        "account_currency": account.currency,
        "projected_profit": projected_profit,
        "loss_per_lot": abs(projected_profit)
    }
def calculate_mt5_projected_loss(
    symbol,
    direction,
    volume,
    entry_price,
    stop_loss
):
    """
    Calculate the projected trade loss using MT5
    for the exact position volume.

    This is a read-only calculation. It does not
    place or execute a trade.
    """

    # Validate trade direction.
    if direction not in ("BUY", "SELL"):
        raise ValueError("Direction must be BUY or SELL.")

    # Validate position volume.
    if not isinstance(volume, (int, float)):
        raise ValueError("Volume must be numeric.")

    if not math.isfinite(volume) or volume <= 0:
        raise ValueError("Volume must be greater than zero.")

    # Select the requested symbol in MT5.
    if not mt5.symbol_select(symbol, True):
        raise RuntimeError(
            f"Could not select MT5 symbol: {symbol}"
        )

    # Choose the appropriate MT5 order type.
    order_type = (
        mt5.ORDER_TYPE_BUY
        if direction == "BUY"
        else mt5.ORDER_TYPE_SELL
    )

    # Calculate projected profit or loss for the exact volume.
    projected_profit = mt5.order_calc_profit(
        order_type,
        symbol,
        float(volume),
        float(entry_price),
        float(stop_loss)
    )

    if projected_profit is None:
        raise RuntimeError(
            f"MT5 could not calculate projected loss for {symbol}."
        )

    if projected_profit >= 0:
        raise ValueError(
            "The specified stop-loss does not produce a projected loss."
        )

    return {
        "symbol": symbol,
        "direction": direction,
        "volume": float(volume),
        "projected_profit": float(projected_profit),
        "projected_trade_loss": abs(float(projected_profit))
    }