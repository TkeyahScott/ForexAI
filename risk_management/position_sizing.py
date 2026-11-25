
# ==========================================
# FOREXAI: POSITION SIZING
# ==========================================

# Handles:
# - Monetary risk calculation
# - Position volume calculation
# - Configurable account risk percentage


import math


# ==========================================
# RISK CONFIGURATION
# ==========================================

# Default percentage of account balance
# that can be risked on a single trade.

DEFAULT_RISK_PERCENTAGE = 1.0


# ==========================================
# POSITION SIZE CALCULATION
# ==========================================

def calculate_position_size(
    account_balance,
    entry_price,
    stop_loss,
    tick_size,
    tick_value,
    risk_percentage=DEFAULT_RISK_PERCENTAGE
):
    """
    Calculate trade volume based on monetary risk.

    Args:
        account_balance (float): Trading account balance.
        entry_price (float): Proposed entry price.
        stop_loss (float): Calculated stop-loss price.
        tick_size (float): Symbol's minimum price movement.
        tick_value (float): Monetary value of one tick
                            for one lot, in account currency.
        risk_percentage (float): Percentage of balance to risk.

    Returns:
        dict: Position sizing calculations.
    """

    # Convert inputs into numerical values.
    try:
        account_balance = float(account_balance)
        entry_price = float(entry_price)
        stop_loss = float(stop_loss)
        tick_size = float(tick_size)
        tick_value = float(tick_value)
        risk_percentage = float(risk_percentage)

    except (TypeError, ValueError):
        raise ValueError(
            "All position sizing inputs must be numeric."
        )

    # Reject NaN and infinite values.
    if not all(
        math.isfinite(value)
        for value in [
            account_balance,
            entry_price,
            stop_loss,
            tick_size,
            tick_value,
            risk_percentage
        ]
    ):
        raise ValueError(
            "Position sizing values must be finite."
        )

    # Validate account balance.
    if account_balance <= 0:
        raise ValueError(
            "Account balance must be greater than zero."
        )

    # Validate entry and stop-loss prices.
    if entry_price <= 0 or stop_loss <= 0:
        raise ValueError(
            "Entry and stop-loss prices must be positive."
        )

    # Stop-loss must differ from entry.
    if entry_price == stop_loss:
        raise ValueError(
            "Entry and stop-loss prices cannot be equal."
        )

    # Validate MT5 symbol specifications.
    if tick_size <= 0 or tick_value <= 0:
        raise ValueError(
            "Tick size and tick value must be positive."
        )

    # Validate risk percentage.
    if not 0 < risk_percentage <= 100:
        raise ValueError(
            "Risk percentage must be greater than 0 and at most 100."
        )

    # Calculate the monetary amount to risk.
    risk_amount = (
        account_balance * risk_percentage / 100
    )

    # Calculate the distance between entry and stop-loss.
    stop_distance = abs(
        entry_price - stop_loss
    )

    # Calculate how many ticks are in the stop distance.
    stop_ticks = stop_distance / tick_size

    # Calculate the monetary risk for one standard lot.
    risk_per_lot = stop_ticks * tick_value

    if risk_per_lot <= 0:
        raise ValueError(
            "Calculated risk per lot must be positive."
        )

    # Calculate the required position volume.
    position_size = risk_amount / risk_per_lot

    # Return the calculations.
    return {
        "account_balance": account_balance,
        "risk_percentage": risk_percentage,
        "risk_amount": risk_amount,
        "stop_distance": stop_distance,
        "risk_per_lot": risk_per_lot,
        "position_size": position_size
    }


def adjust_position_size_to_broker(
    position_size,
    volume_min,
    volume_max,
    volume_step
):
    """
    Adjust calculated trade volume to broker restrictions.

    Volume is rounded DOWN to avoid exceeding
    the originally calculated position size.

    Returns:
        float: Broker-compliant position volume.

    Raises:
        ValueError: If inputs are invalid or the
                    calculated volume is below the minimum.
    """

    # Convert inputs into numerical values.
    try:
        position_size = float(position_size)
        volume_min = float(volume_min)
        volume_max = float(volume_max)
        volume_step = float(volume_step)
    except (TypeError, ValueError):
        raise ValueError("Volume inputs must be numeric.")

    # Reject NaN and infinite values.
    if not all(math.isfinite(value) for value in [
        position_size, volume_min, volume_max, volume_step
    ]):
        raise ValueError("Volume inputs must be finite.")

    if position_size <= 0:
        raise ValueError("Position size must be positive.")

    if volume_min <= 0 or volume_max <= 0 or volume_step <= 0:
        raise ValueError("Broker volume restrictions must be positive.")

    if volume_max < volume_min:
        raise ValueError("Maximum volume cannot be below minimum volume.")

    # Cap volume at the broker's maximum.
    allowed_volume = min(position_size, volume_max)

    # Reject trades that cannot meet the minimum volume
    # without exceeding the planned position size.
    if allowed_volume < volume_min:
        raise ValueError(
            "Calculated position size is below broker minimum. "
            "Trade rejected to protect the risk limit."
        )

    # Calculate the number of permitted steps above minimum.
    steps = math.floor(
        (allowed_volume - volume_min) / volume_step + 1e-10
    )

    # Calculate the final permitted volume.
    adjusted_volume = volume_min + steps * volume_step

    return round(adjusted_volume, 8)