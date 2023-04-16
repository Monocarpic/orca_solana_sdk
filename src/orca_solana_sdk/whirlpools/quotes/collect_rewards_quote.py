import datetime as dt
from typing import Optional, Tuple

from ...whirlpool_idl.accounts import Position, Whirlpool
from ...whirlpool_idl.types import Tick
from ..constants import NUM_REWARDS
from ..utils.math.bit_math import BitMath
from ..utils.pool_utils import PoolUtil


def collect_rewards_quote(
    whirlpool: Whirlpool,
    position: Position,
    tick_lower: Tick,
    tick_upper: Tick,
    timestamp_in_seconds: Optional[int] = None,
) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    cur_ts = (
        timestamp_in_seconds
        if timestamp_in_seconds is not None
        else int(dt.datetime.now().timestamp())
    )
    ts_delta = cur_ts - whirlpool.reward_last_updated_timestamp
    reward_owed = [None, None, None]

    for i in range(NUM_REWARDS):
        try:
            reward_info = whirlpool.reward_infos[i]
        except KeyError:
            raise AssertionError("whirlpool_reward_infos cannot be undefined")
        position_reward_info = position.reward_infos[i]

        is_reward_initialised = PoolUtil.is_reward_initialised(reward_info)
        if not is_reward_initialised:
            continue

        adjusted_reward_growth_global_x64 = reward_info.growth_global_x64
        if whirlpool.liquidity != 0:
            reward_growth_delta = BitMath.mul_div(
                ts_delta, reward_info.emissions_per_second_x64, whirlpool.liquidity, 128
            )
            adjusted_reward_growth_global_x64 += reward_growth_delta

        tick_lower_reward_growths_outside_x64 = tick_lower.reward_growths_outside[i]
        tick_upper_reward_growths_outside_x64 = tick_upper.reward_growths_outside[i]

        reward_growths_below_x64 = adjusted_reward_growth_global_x64
        if tick_lower.initialized:
            if whirlpool.tick_current_index < position.tick_lower_index:
                reward_growths_below_x64 = (
                    adjusted_reward_growth_global_x64
                    - tick_lower_reward_growths_outside_x64
                )
            else:
                reward_growths_below_x64 = tick_lower_reward_growths_outside_x64

        reward_growths_above_x64 = 0
        if tick_upper.initialized:
            if whirlpool.tick_current_index < position.tick_upper_index:
                reward_growths_above_x64 = tick_upper_reward_growths_outside_x64
            else:
                reward_growths_above_x64 = (
                    adjusted_reward_growth_global_x64
                    - tick_upper_reward_growths_outside_x64
                )

        reward_growth_inside_x64 = (
            adjusted_reward_growth_global_x64
            - reward_growths_below_x64
            - reward_growths_above_x64
        )

        amount_owed_x64 = position_reward_info.amount_owed << 64
        reward_owed[i] = (
            amount_owed_x64
            + (
                (
                    reward_growth_inside_x64
                    - position_reward_info.growth_inside_checkpoint
                )
                * position.liquidity
            )
        ) >> 64
    return tuple(reward_owed)
