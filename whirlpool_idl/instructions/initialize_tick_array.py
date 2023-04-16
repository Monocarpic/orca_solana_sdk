from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from ..program_id import PROGRAM_ID


class InitializeTickArrayArgs(typing.TypedDict):
    start_tick_index: int


layout = borsh.CStruct("start_tick_index" / borsh.I32)


class InitializeTickArrayAccounts(typing.TypedDict):
    whirlpool: Pubkey
    funder: Pubkey
    tick_array: Pubkey


def initialize_tick_array(
    args: InitializeTickArrayArgs,
    accounts: InitializeTickArrayAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["whirlpool"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["funder"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["tick_array"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x0b\xbc\xc1\xd6\x8d[\x95\xb8"
    encoded_args = layout.build(
        {
            "start_tick_index": args["start_tick_index"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
