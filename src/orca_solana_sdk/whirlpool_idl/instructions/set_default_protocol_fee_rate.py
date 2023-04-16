from __future__ import annotations

import typing

import borsh_construct as borsh
from solders.instruction import AccountMeta, Instruction
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class SetDefaultProtocolFeeRateArgs(typing.TypedDict):
    default_protocol_fee_rate: int


layout = borsh.CStruct("default_protocol_fee_rate" / borsh.U16)


class SetDefaultProtocolFeeRateAccounts(typing.TypedDict):
    whirlpools_config: Pubkey
    fee_authority: Pubkey


def set_default_protocol_fee_rate(
    args: SetDefaultProtocolFeeRateArgs,
    accounts: SetDefaultProtocolFeeRateAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(
            pubkey=accounts["whirlpools_config"], is_signer=False, is_writable=True
        ),
        AccountMeta(
            pubkey=accounts["fee_authority"], is_signer=True, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"k\xcd\xf9\xe2\x97#V\x00"
    encoded_args = layout.build(
        {
            "default_protocol_fee_rate": args["default_protocol_fee_rate"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
