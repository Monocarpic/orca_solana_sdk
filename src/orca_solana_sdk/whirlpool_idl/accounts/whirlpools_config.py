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


class WhirlpoolsConfigJSON(typing.TypedDict):
    fee_authority: str
    collect_protocol_fees_authority: str
    reward_emissions_super_authority: str
    default_protocol_fee_rate: int


@dataclass
class WhirlpoolsConfig:
    discriminator: typing.ClassVar = b"\x9d\x141\xe0\xd9W\xc1\xfe"
    layout: typing.ClassVar = borsh.CStruct(
        "fee_authority" / BorshPubkey,
        "collect_protocol_fees_authority" / BorshPubkey,
        "reward_emissions_super_authority" / BorshPubkey,
        "default_protocol_fee_rate" / borsh.U16,
    )
    fee_authority: Pubkey
    collect_protocol_fees_authority: Pubkey
    reward_emissions_super_authority: Pubkey
    default_protocol_fee_rate: int

    @classmethod
    async def fetch(
        cls,
        conn: AsyncClient,
        address: Pubkey,
        commitment: typing.Optional[Commitment] = None,
        program_id: Pubkey = PROGRAM_ID,
    ) -> typing.Optional["WhirlpoolsConfig"]:
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
    ) -> typing.List[typing.Optional["WhirlpoolsConfig"]]:
        infos = await get_multiple_accounts(conn, addresses, commitment=commitment)
        res: typing.List[typing.Optional["WhirlpoolsConfig"]] = []
        for info in infos:
            if info is None:
                res.append(None)
                continue
            if info.account.owner != program_id:
                raise ValueError("Account does not belong to this program")
            res.append(cls.decode(info.account.data))
        return res

    @classmethod
    def decode(cls, data: bytes) -> "WhirlpoolsConfig":
        if data[:ACCOUNT_DISCRIMINATOR_SIZE] != cls.discriminator:
            raise AccountInvalidDiscriminator(
                "The discriminator for this account is invalid"
            )
        dec = WhirlpoolsConfig.layout.parse(data[ACCOUNT_DISCRIMINATOR_SIZE:])
        return cls(
            fee_authority=dec.fee_authority,
            collect_protocol_fees_authority=dec.collect_protocol_fees_authority,
            reward_emissions_super_authority=dec.reward_emissions_super_authority,
            default_protocol_fee_rate=dec.default_protocol_fee_rate,
        )

    def to_json(self) -> WhirlpoolsConfigJSON:
        return {
            "fee_authority": str(self.fee_authority),
            "collect_protocol_fees_authority": str(
                self.collect_protocol_fees_authority
            ),
            "reward_emissions_super_authority": str(
                self.reward_emissions_super_authority
            ),
            "default_protocol_fee_rate": self.default_protocol_fee_rate,
        }

    @classmethod
    def from_json(cls, obj: WhirlpoolsConfigJSON) -> "WhirlpoolsConfig":
        return cls(
            fee_authority=Pubkey.from_string(obj["fee_authority"]),
            collect_protocol_fees_authority=Pubkey.from_string(
                obj["collect_protocol_fees_authority"]
            ),
            reward_emissions_super_authority=Pubkey.from_string(
                obj["reward_emissions_super_authority"]
            ),
            default_protocol_fee_rate=obj["default_protocol_fee_rate"],
        )
