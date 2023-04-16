from ..whirlpool_idl.accounts import Position, Whirlpool
from typing import Optional
from ..whirlpool_idl.types import Tick
from dataclasses import dataclass


@dataclass
class CollectFeesQuote:
    fee_owed_a: int
    fee_owed_b: int


def collect_fees_quote(
    whirlpool: Whirlpool, position: Position, tick_lower: Tick, tick_upper: Tick
):
    fee_growth_below_ax64: Optional[int] = None
    fee_growth_below_bx64: Optional[int] = None

    if whirlpool.tick_current_index < position.tick_lower_index:
        fee_growth_below_ax64 = (
            whirlpool.fee_growth_global_a - tick_lower.fee_growth_outside_a
        )
        fee_growth_below_bx64 = (
            whirlpool.fee_growth_global_b - tick_lower.fee_growth_outside_b
        )
    else:
        fee_growth_below_ax64 = tick_lower.fee_growth_outside_a
        fee_growth_below_bx64 = tick_lower.fee_growth_outside_b

    fee_growth_above_ax64: Optional[int] = None
    fee_growth_above_bx64: Optional[int] = None

    if whirlpool.tick_current_index < position.tick_upper_index:
        fee_growth_above_ax64 = tick_upper.fee_growth_outside_a
        fee_growth_above_bx64 = tick_upper.fee_growth_outside_b
    else:
        fee_growth_above_ax64 = (
            whirlpool.fee_growth_global_a - tick_upper.fee_growth_outside_a
        )
        fee_growth_above_bx64 = (
            whirlpool.fee_growth_global_b - tick_upper.fee_growth_outside_b
        )

    fee_growth_inside_ax64 = (
        whirlpool.fee_growth_global_a - fee_growth_below_ax64 - fee_growth_above_ax64
    )
    fee_growth_inside_bx64 = (
        whirlpool.fee_growth_global_b - fee_growth_below_bx64 - fee_growth_above_bx64
    )

    fee_owed_a_delta = (
        (fee_growth_inside_ax64 - position.fee_growth_checkpoint_a) * position.liquidity
    ) >> 64
    fee_owed_b_delta = (
        (fee_growth_inside_bx64 - position.fee_growth_checkpoint_b) * position.liquidity
    ) >> 64

    updated_fee_owned_a = position.fee_owed_a + fee_owed_a_delta
    updated_fee_owned_b = position.fee_owed_b + fee_owed_b_delta

    return CollectFeesQuote(
        fee_owed_a=updated_fee_owned_a, fee_owed_b=updated_fee_owned_b
    )
