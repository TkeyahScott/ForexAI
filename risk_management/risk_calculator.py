# ==========================================
# FOREXAI: RISK CALCULATOR
# ==========================================

# Handles:
# - ATR-based stop-loss calculations
# - Risk/reward calculations
# - Take-profit calculations

import math


# ==========================================
# RISK MANAGEMENT CONFIGURATION
# ==========================================

# Initial stop-loss distance multiplier.
ATR_STOP_MULTIPLIER = 1.5

# Initial risk/reward target.
RISK_REWARD_RATIO = 2.0


# ==========================================
# STOP-LOSS AND TAKE-PROFIT CALCULATION
# ==========================================

def calculate_stop_loss_take_profit(
    entry_price,
    direction,
    atr,
    stop_multiplier=ATR_STOP_MULTIPLIER,
    risk_reward_ratio=RISK_REWARD_RATIO
):
    """
    Calculate stop-loss and take-profit prices.

    Args:
        entry_price (float): Proposed trade entry price.
        direction (str): BUY or SELL.
        atr (float): M15 ATR14 value.
        stop_multiplier (float): ATR stop-loss multiplier.
        risk_reward_ratio (float): Target risk/reward ratio.

    Returns:
        dict: Trade risk and reward calculations.
    """

    # Convert inputs into numerical values.
    try:
        entry_price = float(entry_price)
        atr = float(atr)
        stop_multiplier = float(stop_multiplier)
        risk_reward_ratio = float(risk_reward_ratio)

    except (TypeError, ValueError):
        raise ValueError(
            "Entry price, ATR and multipliers must be numeric."
        )

    # Reject invalid numerical values.
    if not all(
        math.isfinite(value)
        for value in [
            entry_price,
            atr,
            stop_multiplier,
            risk_reward_ratio
        ]
    ):
        raise ValueError(
            "Calculation values must be finite numbers."
        )

    # Validate the entry price.
    if entry_price <= 0:
        raise ValueError(
            "Entry price must be greater than zero."
        )

    # ATR must be positive.
    if atr <= 0:
        raise ValueError(
            "ATR must be greater than zero."
        )

    # Multipliers must be positive.
    if stop_multiplier <= 0:
        raise ValueError(
            "Stop multiplier must be greater than zero."
        )

    if risk_reward_ratio <= 0:
        raise ValueError(
            "Risk/reward ratio must be greater than zero."
        )

    # Validate trade direction.
    direction = direction.upper()

    if direction not in ["BUY", "SELL"]:
        raise ValueError(
            "Direction must be BUY or SELL."
        )

    # Calculate the stop-loss distance using ATR.
    stop_distance = atr * stop_multiplier

    # Calculate the take-profit distance.
    reward_distance = (
        stop_distance * risk_reward_ratio
    )

    # Calculate prices for a BUY trade.
    if direction == "BUY":

        stop_loss = entry_price - stop_distance

        take_profit = entry_price + reward_distance

    # Calculate prices for a SELL trade.
    else:

        stop_loss = entry_price + stop_distance

        take_profit = entry_price - reward_distance

    # Return the calculated trade levels.
    return {
        "direction": direction,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "stop_distance": stop_distance,
        "reward_distance": reward_distance,
        "risk_reward_ratio": risk_reward_ratio
    }