import asyncio
from typing import List

from ..whirlpool_idl.accounts import Position, Whirlpool
from .context import WhirlpoolContext
from .network.fetcher import AccountFetcher


class WhirlpoolClient:
    def __init__(self, context: WhirlpoolContext):
        self._context = context

    def get_context(self) -> WhirlpoolContext:
        return self._context

    def get_fetcher(self) -> AccountFetcher:
        return self._context.fetcher

    # TODO: implement type Address
    async def get_pool(self, pool_address, refresh: bool = False) -> Whirlpool:
        return await self._context.fetcher.get_pool(pool_address, refresh)

    # TODO: implement type Address
    async def get_pools(self, pool_addresses, refresh: bool = False) -> List[Whirlpool]:
        return await asyncio.gather(
            *[self._context.fetcher.get_pool(pa, refresh) for pa in pool_addresses]
        )

    async def get_position(self, position_address, refresh: bool = False) -> Position:
        return await self._context.fetcher.get_position(position_address, refresh)

    async def get_positions(
        self, position_addresses, refresh: bool = False
    ) -> List[Position]:
        return await asyncio.gather(
            *[
                self._context.fetcher.get_position(pa, refresh)
                for pa in position_addresses
            ]
        )

    async def collect_fees_and_rewards_for_positions(self):
        raise NotImplementedError()

    async def create_pool(self):
        raise NotImplementedError()


def build_whirlpool_client(context: WhirlpoolContext) -> WhirlpoolClient:
    return WhirlpoolClient(context)
