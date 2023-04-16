from dataclasses import dataclass
from solders.pubkey import Pubkey


@dataclass
class PDA:
    public_key: Pubkey
    bump: int
