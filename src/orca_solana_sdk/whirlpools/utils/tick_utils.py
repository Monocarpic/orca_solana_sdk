import math

from solders.pubkey import Pubkey

from ...whirlpool_idl.accounts import TickArray
from ...whirlpool_idl.types import Tick
from ..constants import MAX_TICK_INDEX, MIN_TICK_INDEX, TICK_ARRAY_SIZE
from .pda_utils import PDAUtil


class TickUtil:
    @staticmethod
    def get_start_tick_index(
        tick_index: int, tick_spacing: int, offset: int = 0
    ) -> int:
        real_index = math.floor(tick_index / tick_spacing / TICK_ARRAY_SIZE)
        start_tick_index = (real_index + offset) * tick_spacing * TICK_ARRAY_SIZE

        ticks_in_array = TICK_ARRAY_SIZE * tick_spacing
        min_tick_index = MIN_TICK_INDEX - (
            (MIN_TICK_INDEX % ticks_in_array) + ticks_in_array
        )
        assert (
            start_tick_index >= min_tick_index
        ), f"start_tick_index is too small - {start_tick_index}"
        assert (
            start_tick_index <= MAX_TICK_INDEX
        ), f"start_tick_index is too large - {start_tick_index}"
        return start_tick_index

    @staticmethod
    def get_tick_array_pdas(
        tick: int,
        tick_spacing: int,
        num_of_tick_arrays: int,
        program_id: Pubkey,
        whirlpool_address: Pubkey,
        a_to_b: bool,
    ):
        array_index_list = []
        for _i in range(num_of_tick_arrays):
            array_index_list.append(_i * (-1 if a_to_b else 1))

        def get_pda_tick_array(offset):
            start_tick = TickUtil.get_start_tick_index(tick, tick_spacing, offset)
            return PDAUtil.get_tick_array(program_id, whirlpool_address, start_tick)

        return [get_pda_tick_array(x) for x in array_index_list]


class TickArrayUtil:
    @staticmethod
    def get_tick_from_array(
        tick_array: TickArray,
        tick_index: int,
        tick_spacing: int,
    ) -> Tick:
        real_index = tick_index_to_inner_index(
            tick_array.start_tick_index, tick_index, tick_spacing
        )
        try:
            tick = tick_array.ticks[real_index]
        except KeyError:
            raise AssertionError(
                "tick real_index out of range - "
                f"start - {tick_array.start_tick_index} "
                f"index - {tick_index}, "
                f"realIndex - {real_index}"
            )
        return tick


def tick_index_to_inner_index(
    start_tick_index: int,
    tick_index: int,
    tick_spacing: int,
) -> int:
    return math.floor((tick_index - start_tick_index) / tick_spacing)
