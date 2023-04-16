from solders.pubkey import Pubkey

from ...whirlpool_idl.types.whirlpool_reward_info import WhirlpoolRewardInfo

# TODO: probably want to find a better place to put this
# https://github.com/solana-labs/solana-web3.js/blob/master/packages/library-legacy/src/publickey.ts#L91
DEFAULT_PUBKEY_ADDRESS = Pubkey.from_string("11111111111111111111111111111111")


class PoolUtil:
    @staticmethod
    def is_reward_initialised(reward_info: WhirlpoolRewardInfo) -> bool:
        return (
            reward_info.mint != DEFAULT_PUBKEY_ADDRESS
            and reward_info.vault != DEFAULT_PUBKEY_ADDRESS
        )
