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

