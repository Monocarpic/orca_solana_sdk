from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID

from ..program_id import PROGRAM_ID


class DecreaseLiquidityArgs(typing.TypedDict):
    liquidity_amount: int
    token_min_a: int
    token_min_b: int


layout = borsh.CStruct(
    "liquidity_amount" / borsh.U128,
    "token_min_a" / borsh.U64,
    "token_min_b" / borsh.U64,
)


class DecreaseLiquidityAccounts(typing.TypedDict):
    whirlpool: Pubkey
    position_authority: Pubkey
    position: Pubkey
    position_token_account: Pubkey
    token_owner_account_a: Pubkey
    token_owner_account_b: Pubkey
    token_vault_a: Pubkey
    token_vault_b: Pubkey
    tick_array_lower: Pubkey
    tick_array_upper: Pubkey


def decrease_liquidity(
    args: DecreaseLiquidityArgs,
    accounts: DecreaseLiquidityAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["whirlpool"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=accounts["position_authority"], is_signer=True, is_writable=False
        ),
        AccountMeta(pubkey=accounts["position"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["position_token_account"],
            is_signer=False,
            is_writable=False,
        ),
        AccountMeta(
            pubkey=accounts["token_owner_account_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_owner_account_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_vault_a"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["token_vault_b"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["tick_array_lower"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["tick_array_upper"], is_signer=False, is_writable=True
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xa0&\xd0oh[,\x01"
    encoded_args = layout.build(
        {
            "liquidity_amount": args["liquidity_amount"],
            "token_min_a": args["token_min_a"],
            "token_min_b": args["token_min_b"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
