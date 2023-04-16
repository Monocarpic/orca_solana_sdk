from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class OpenPositionArgs(typing.TypedDict):
    bumps: types.open_position_bumps.OpenPositionBumps
    tick_lower_index: int
    tick_upper_index: int


layout = borsh.CStruct(
    "bumps" / types.open_position_bumps.OpenPositionBumps.layout,
    "tick_lower_index" / borsh.I32,
    "tick_upper_index" / borsh.I32,
)


class OpenPositionAccounts(typing.TypedDict):
    funder: Pubkey
    owner: Pubkey
    position: Pubkey
    position_mint: Pubkey
    position_token_account: Pubkey
    whirlpool: Pubkey


def open_position(
    args: OpenPositionArgs,
    accounts: OpenPositionAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["funder"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["owner"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["position"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["position_mint"], is_signer=True, is_writable=True),
        AccountMeta(
            pubkey=accounts["position_token_account"], is_signer=False, is_writable=True
        ),
        AccountMeta(pubkey=accounts["whirlpool"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(
            pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False
        ),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x87\x80/M\x0f\x98\xf01"
    encoded_args = layout.build(
        {
            "bumps": args["bumps"].to_encodable(),
            "tick_lower_index": args["tick_lower_index"],
            "tick_upper_index": args["tick_upper_index"],
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
