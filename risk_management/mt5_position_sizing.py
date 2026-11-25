
# ==========================================
# FOREXAI: MT5 POSITION SIZING
# ==========================================

# Handles:
# - Retrieving actual MT5 account information.
# - Calculating monetary loss using MT5.
# - Calculating theoretical position volume.
# - Adjusting volume to broker restrictions.
#
# This module is READ-ONLY.
# It does not place trades.

import math

import MetaTrader5 as mt5

from risk_management.mt5_risk_data import get_mt5_risk_data

from risk_management.mt5_profit_calculator import (
    calculate_mt5_loss_per_lot,
    calculate_mt5_projected_loss
)

from risk_management.position_sizing import (
    adjust_position_size_to_broker
)


def calculate_mt5_position_size(
    symbol,
    direction,
    entry_price,
    stop_loss,
    risk_percentage=1.0
):
    """
    Calculate position size using actual MT5 data.

    MT5 must already be initialized.

    Returns:
        dict: Account risk and broker-adjusted position size.
    """

    # Convert and validate the risk percentage.
    try:
        risk_percentage = float(risk_percentage)
    except (TypeError, ValueError):
        raise ValueError("Risk percentage must be numeric.")

    if not math.isfinite(risk_percentage):
        raise ValueError("Risk percentage must be finite.")

    if not 0 < risk_percentage <= 100:
        raise ValueError(
            "Risk percentage must be greater than 0 and at most 100."
        )

    # Retrieve account and broker specifications.
    risk_data = get_mt5_risk_data(symbol)

    # Calculate the actual projected loss for one lot.
    loss_data = calculate_mt5_loss_per_lot(
        symbol=symbol,
        direction=direction,
        entry_price=entry_price,
        stop_loss=stop_loss
    )

    # Calculate the monetary risk allowance.
    risk_amount = (
        risk_data["account_balance"] * risk_percentage / 100
    )

    # Calculate theoretical position volume.
    theoretical_position_size = (
        risk_amount / loss_data["loss_per_lot"]
    )

    # Adjust volume to broker restrictions.
    adjusted_volume = adjust_position_size_to_broker(
        position_size=theoretical_position_size,
        volume_min=risk_data["volume_min"],
        volume_max=risk_data["volume_max"],
        volume_step=risk_data["volume_step"]
    )
    # Calculate the projected loss using the final broker-adjusted volume.
    final_loss_data = calculate_mt5_projected_loss(
        symbol=symbol,
        direction=direction,
        volume=adjusted_volume,
        entry_price=entry_price,
        stop_loss=stop_loss
    )

    # Retrieve the projected loss calculated by MT5.
    projected_trade_loss = final_loss_data["projected_trade_loss"]

    # Prevent a position from exceeding the permitted risk amount.
    if projected_trade_loss > risk_amount:
        raise ValueError(
            "Projected trade loss exceeds the permitted risk amount."
        )

    # Calculate the projected loss using the final volume.
    projected_trade_loss = (
        loss_data["loss_per_lot"] * adjusted_volume
    )

    # Return the complete calculation.
    return {
        **risk_data,
        "direction": loss_data["direction"],
        "entry_price": float(entry_price),
        "stop_loss": float(stop_loss),
        "risk_percentage": risk_percentage,
        "risk_amount": risk_amount,
        "loss_per_lot": loss_data["loss_per_lot"],
        "theoretical_position_size": theoretical_position_size,
        "position_size": adjusted_volume,
        "final_loss_data": final_loss_data,
        "projected_trade_loss": projected_trade_loss
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

        # Ask MT5 to calculate the projected profit or loss
        # using the exact adjusted position volume.
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