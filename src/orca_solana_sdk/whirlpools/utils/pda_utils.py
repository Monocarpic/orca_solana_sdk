from solders.pubkey import Pubkey

from ...common.address_utils import AddressUtil
from ...common.classes import PDA

PDA_WHIRLPOOL_SEED = "whirlpool"
PDA_TICK_ARRAY_SEED = "tick_array"
PDA_FEE_TIER_SEED  = "fee_tier"


class PDAUtil:
    @staticmethod
    def get_whirlpool(
        program_id: Pubkey,
        whirlpool_configs_key: Pubkey,
        token_mint_a_key: Pubkey,
        token_mint_b_key: Pubkey,
        tick_spacing: int,
    ):
        # TODO: do we want some sanity check on the order of token_mint_a_key and token_mint_b_key?
        return AddressUtil.find_program_address(
            [
                PDA_WHIRLPOOL_SEED.encode(),
                bytes(whirlpool_configs_key),
                bytes(token_mint_a_key),
                bytes(token_mint_b_key),
                tick_spacing.to_bytes(2, "little"),
            ],
            program_id,
        )

    @staticmethod
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

    @staticmethod
    def get_fee_tier(
        program_id: Pubkey,
        whirlpools_config_address: Pubkey,
        tick_spacing: int
    ):
        return AddressUtil.find_program_address(
            [
                PDA_FEE_TIER_SEED.encode(),
                bytes(whirlpools_config_address),
                tick_spacing.to_bytes(2, "little"),
            ],
            program_id
        )