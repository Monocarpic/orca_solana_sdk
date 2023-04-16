import typing
from dataclasses import dataclass

import borsh_construct as borsh
from anchorpy.borsh_extension import BorshPubkey
from anchorpy.coder.accounts import ACCOUNT_DISCRIMINATOR_SIZE
from anchorpy.error import AccountInvalidDiscriminator
from anchorpy.utils.rpc import get_multiple_accounts
from solana.rpc.async_api import AsyncClient
from solana.rpc.commitment import Commitment
from solders.pubkey import Pubkey

from ..program_id import PROGRAM_ID


class FeeTierJSON(typing.TypedDict):
    whirlpools_config: str
    tick_spacing: int
    default_fee_rate: int


@dataclass
class FeeTier:
    discriminator: typing.ClassVar = b"8K\x9fL\x8eD\xbei"
    layout: typing.ClassVar = borsh.CStruct(
        "whirlpools_config" / BorshPubkey,
        "tick_spacing" / borsh.U16,
        "default_fee_rate" / borsh.U16,
    )
    whirlpools_config: Pubkey
    tick_spacing: int
    default_fee_rate: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["FeeTier"]:
        resp = await conn.get_account_info(address, commitment=commitment)
        info = resp.value
        if info is None:
            return None
        if info.owner != program_id:
            raise ValueError("Account does not belong to this program")
        bytes_data = info.data
        return cls.decode(bytes_data)

    @classmethod
    async def fetch_multiple(
        cls,
        conn: AsyncClient,
        addresses: list[Pubkey],
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.List[typing.Optional["FeeTier"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["FeeTier"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "FeeTier":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = FeeTier.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            whirlpools_config=dec.whirlpools_config,
            tick_spacing=dec.tick_spacing,
            default_fee_rate=dec.default_fee_rate,
        )

    def to_json(self) -> FeeTierJSON:
        return {
            "whirlpools_config": str(self.whirlpools_config),
            "tick_spacing": self.tick_spacing,
            "default_fee_rate": self.default_fee_rate,
        }

    @classmethod
    def from_json(cls, obj: FeeTierJSON) -> "FeeTier":
        return cls(
            whirlpools_config=Pubkey.from_string(obj["whirlpools_config"]),
            tick_spacing=obj["tick_spacing"],
            default_fee_rate=obj["default_fee_rate"],
        )
