from solders.pubkey import Pubkey

from ...common.address_utils import AddressUtil
from ...common.classes import PDA

PDA_TICK_ARRAY_SEED = "tick_array"


class PDAUtil:
    def get_tick_array(
        program_id: Pubkey, whirlpool_address: Pubkey, start_tick: int
    ) -> PDA:
        return AddressUtil.find_program_address(
            [
                PDA_TICK_ARRAY_SEED.encode(),
                bytes(whirlpool_address),
                str(start_tick).encode(),
            ],
            program_id,
        )
