from .network.fetcher import AccountFetcher


class WhirlpoolContext:
    def __init__(self, fetcher: AccountFetcher):
        self.fetcher = fetcher
