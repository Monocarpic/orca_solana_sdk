from solders.pubkey import Pubkey
from .classes import PDA
from typing import Sequence


class AddressUtil:
    @staticmethod
    def find_program_address(seeds: Sequence[bytes], program_id: Pubkey) -> PDA:
        return PDA(*Pubkey.find_program_address(seeds, program_id))
