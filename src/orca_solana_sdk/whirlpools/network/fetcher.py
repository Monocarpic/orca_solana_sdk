from dataclasses import dataclass
from typing import Dict, Optional, Type, Union

import base58
from solana.rpc.api import Client
from solders.pubkey import Pubkey

from ...whirlpool_idl.accounts.whirlpools_config import WhirlpoolsConfig


class AccountFetcher:
    def __init__(self, connection: Client, cache: Optional[Dict] = None):
        self.connection = connection
        self._cache = cache if cache else {}

    async def get_config(self, address: Union[Pubkey, str], refresh: bool = False):
        try:
            address = Pubkey.from_string(address)
        except TypeError:
            pass
        return await self._get(address, WhirlpoolsConfig, refresh)

    async def _get(
        self, address: Pubkey, entity: Type[dataclass], refresh: bool
    ) -> dataclass:
        key = base58.b58encode(str(address))

        # TODO: think caching logic was not reimplemented properly
        cached_value = self._cache.get(key)

        if cached_value is not None and not refresh:
            return cached_value

        account_info = await self.connection.get_account_info(address)
        account_data = account_info.value.data

        value = entity.decode(account_data)
        if key in self._cache:
            self._cache[key][entity] = value
        else:
            self._cache[key] = {entity: value}

        return value
