# market.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, Union,
    Any, ClassVar, List, Tuple, TypeVar, Type
)

from attrs import define

from represent import represent, Modifiers

import numpy as np
import pandas as pd

from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.orderbook import OrderbookScreener
from crypto_screening.dataset import BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME
from crypto_screening.symbols import symbol_to_parts, parts_to_symbol
from crypto_screening.collect.screeners import find_screeners
from crypto_screening.market.screeners.orderbook import create_orderbook_dataframe

__all__ = [
    "validate_assets_market_state_prices_symbol",
    "assets_market_price",
    "is_symbol_in_assets_market_prices",
    "symbols_market_prices",
    "symbols_market_state",
    "symbols_market_price",
    "merge_assets_market_states",
    "merge_symbols_market_states",
    "assets_market_prices",
    "validate_symbols_market_state_prices_symbol",
    "assets_market_state",
    "AssetsMarketState",
    "SymbolsMarketState",
    "is_exchange_in_market_prices",
    "is_symbol_in_symbols_market_prices",
    "symbol_market_prices_to_assets_market_prices",
    "symbols_market_state_to_assets_market_state",
    "assets_market_state_to_symbols_market_state",
    "assets_market_prices_to_symbol_market_prices",
    "assets_market_dataset_to_symbols_market_datasets",
    "symbols_market_dataset_to_assets_market_datasets",
    "symbols_screeners",
    "symbols_market_datasets_to_symbols_screeners",
    "assets_screeners",
    "assets_market_datasets_to_assets_screeners",
    "assets_market_data_to_symbols_market_data",
    "add_symbols_data_to_screeners",
    "add_assets_data_to_screeners",
    "symbols_market_data_to_assets_market_data",
    "merge_symbols_market_data",
    "merge_assets_market_data"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]

def is_exchange_in_market_prices(
        exchange: str,
        prices: Union[AssetsPrices, SymbolsPrices]
) -> None:
    """
    Checks if the exchange is in the prices.

    :param exchange: The exchange name.
    :param prices: The prices.

    :return: The boolean flag.
    """

    return exchange not in prices
# end is_exchange_in_market_prices

def is_symbol_in_assets_market_prices(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param separator: The separator of the assets.

    :return: The validation value.
    """

    if not is_exchange_in_market_prices(exchange=exchange, prices=prices):
        return False
    # end if

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if base not in prices[exchange]:
        return False
    # end if

    if quote not in prices[exchange][base]:
        return False
    # end if

    return not np.isnan(prices[exchange][base][quote])
# end is_symbol_in_assets_market_prices

def is_symbol_in_symbols_market_prices(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices
) -> bool:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.

    :return: The validation value.
    """

    if not is_exchange_in_market_prices(exchange=exchange, prices=prices):
        return False
    # end if

    if symbol not in prices[exchange]:
        return False
    # end if

    return not np.isnan(prices[exchange][symbol])
# end is_symbol_in_assets_market_prices

def validate_assets_market_state_prices_symbol(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if exchange not in prices:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(prices.keys())}"
        )
    # end if

    if base not in prices[exchange]:
        raise ValueError(
            f"base asset '{base}' is not found in '{exchange}' prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found base '{exchange}' assets are: "
            f"{', '.join(prices[exchange].keys())}"
        )
    # end if

    if quote not in prices[exchange][base]:
        raise ValueError(
            f"quote asset '{quote}' is not found in the quote "
            f"assets of the '{base}' base asset in the prices"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found quote assets for the '{base}' base asset in "
            f"the prices are: {', '.join(prices[exchange][base].keys())}"
        )
    # end if
# end validate_assets_market_state_prices_symbol

def validate_symbols_market_state_prices_symbol(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    if exchange not in prices:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(prices.keys())}"
        )
    # end if

    if symbol not in prices[exchange]:
        raise ValueError(
            f"symbol '{symbol}' is not found in '{exchange}' prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found symbols for '{exchange}' prices are: "
            f"{', '.join(prices[exchange].keys())}"
        )
    # end if
# end validate_symbols_market_state_prices_symbol

def assets_market_price(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, float]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_prices_symbol(
        symbol=symbol, prices=prices, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    data = list(prices[exchange][base][quote])

    return data[-1][0], float(data[-1][-1])
# end assets_market_price

def symbols_market_price(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, float]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_prices_symbol(
        exchange=exchange, symbol=symbol,
        prices=prices, provider=provider
    )

    data = list(prices[exchange][symbol])

    return data[-1][0], float(data[-1][-1])
# end symbols_market_price

@define(repr=False)
@represent
class AssetsMarketBase(metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.
    """

    screeners: Iterable[BaseScreener]

    __modifiers__: ClassVar[Modifiers] = Modifiers(excluded=["screeners"])

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def in_bids_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_prices(
            exchange=exchange, symbol=symbol,
            separator=separator, prices=self.bids
        )
    # end in_bids_prices

    def in_asks_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_prices(
            exchange=exchange, symbol=symbol,
            separator=separator, prices=self.asks
        )
    # end in_asks_prices

    def in_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return (
            self.in_bids_prices(
                exchange=exchange, symbol=symbol,
                separator=separator
            )
            and
            self.in_asks_prices(
                exchange=exchange, symbol=symbol,
                separator=separator
            )
        )
    # end in_prices
# end AssetsMarketBase

@define(repr=False)
@represent
class SymbolsMarketBase(metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.
    """

    screeners: Iterable[BaseScreener]

    __modifiers__: ClassVar[Modifiers] = Modifiers(excluded=["screeners"])

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__

    def in_bids_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids
        )
    # end in_bids_prices

    def in_asks_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks
        )
    # end in_asks_prices

    def in_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return (
            self.in_bids_prices(exchange=exchange, symbol=symbol) and
            self.in_asks_prices(exchange=exchange, symbol=symbol)
        )
    # end in_prices
# end SymbolsMarketBase

def symbols_market_prices(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, float]]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_prices_symbol(
        exchange=exchange, symbol=symbol,
        prices=prices, provider=provider
    )

    return [(time, float(value)) for time, value in prices[exchange][symbol]]
# end symbols_market_prices

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsMarketState(AssetsMarketBase):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    - bids_volume:
        The bids volume prices of the assets.

    - asks_volume:
        The asks volume prices of the assets.

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(...)
    """

    bids: AssetsPrices
    asks: AssetsPrices
    bids_volume: AssetsPrices
    asks_volume: AssetsPrices

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **AssetsMarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks", "bids_volume", "asks_volume"])

    def bid(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids,
            separator=separator, provider=self
        )
    # end bid

    def ask(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks,
            separator=separator, provider=self
        )
    # end ask

    def bid_volume(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids_volume,
            separator=separator, provider=self
        )
    # end bid_volume

    def ask_volume(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks_volume,
            separator=separator, provider=self
        )
    # end ask_volume

    def data(self) -> AssetsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        datasets: Dict[str, Dict[str, Dict[str, Dict[dt.datetime, Dict[str, float]]]]] = {}

        for key, data in zip(
            (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME),
            (self.bids, self.asks, self.bids_volume, self.asks_volume)
        ):
            for exchange, bases in data.items():
                for base, quotes in bases.items():
                    for quote, prices in quotes.items():
                        for i, (time, price) in enumerate(prices):
                            try:
                                if isinstance(time, str):
                                    time = dt.datetime.fromisoformat(time)

                                elif isinstance(time, int):
                                    time = dt.datetime.fromtimestamp(time)

                            except (Type, ValueError):
                                pass
                            # end try

                            (
                                datasets.
                                setdefault(exchange, {}).
                                setdefault(base, {}).
                                setdefault(quote, {}).
                                setdefault(time, {})
                            )[key] = price
                        # end for
                # end for
            # end for
        # end for

        new_datasets: AssetsMarketData = {}

        for exchange, bases in datasets.items():
            for base, quotes in bases.items():
                for quote, prices in quotes.items():
                    (
                        new_datasets.
                        setdefault(exchange, {}).
                        setdefault(base, {})
                    )[quote] = sorted(
                        list(prices.items()), key=lambda pair: pair[0]
                    )
                # end for
            # end for
        # end for

        return new_datasets
    # end data

    def datasets(self) -> AssetsMarketDatasets:
        """
        Rebuilds the dataset from the market state.

        :return: The dataset of the state data.
        """

        datasets: AssetsMarketDatasets = {}

        for exchange, bases in self.data().items():
            for base, quotes in bases.items():
                for quote, rows in quotes.items():
                    dataset = create_orderbook_dataframe()

                    for time, row in rows:
                        dataset.loc[time] = row
                    # end for
                # end for
            # end for
        # end for

        return datasets
# end assets_market_state_to_datasets
# end AssetsMarketStates

def assets_market_prices(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, float]]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_prices_symbol(
        symbol=symbol, prices=prices, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return [(time, float(value)) for time, value in prices[exchange][base][quote]]
# end assets_market_prices

def assets_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    bids: AssetsPrices = {}
    asks: AssetsPrices = {}
    bids_volume: AssetsPrices = {}
    asks_volume: AssetsPrices = {}

    if (length is None) and (not adjust):
        length = min([len(screener.market) for screener in screeners])
    # end if

    for screener in screeners:
        if adjust and (length is None):
            length = len(screener.market)

        elif adjust:
            length = min([len(screener.market), length])
        # end if

        if length > len(screener.market):
            raise ValueError(
                f"Data of '{screener.exchange}' "
                f"symbol in '{screener.symbol}' exchange "
                f"is not long enough for the requested length: {length}. "
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end if

        base, quote = symbol_to_parts(
            symbol=screener.symbol, separator=separator
        )

        for key, data in zip(
            (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME),
            (bids, asks, bids_volume, asks_volume)
        ):
            (
                data.
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(
                    quote,
                    list(
                        zip(
                            list(screener.market.index[-length:]),
                            list(screener.market[key][-length:])
                        )
                    )
                )
            )
    # end for

    return AssetsMarketState(
        screeners=screeners, bids=bids, asks=asks,
        bids_volume=bids_volume, asks_volume=asks_volume
    )
# end assets_market_state

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsMarketState(SymbolsMarketBase):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.

    - prices:
        The close price of the assets.

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    - bids_volume:
        The bids volume prices of the assets.

    - asks_volume:
        The asks volume prices of the assets.

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(...)
    """

    bids: SymbolsPrices
    asks: SymbolsPrices
    bids_volume: SymbolsPrices
    asks_volume: SymbolsPrices

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **AssetsMarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks", "bids_volume", "asks_volume"])

    def bid(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.bids, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.asks, provider=self
        )
    # end ask

    def bid_volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.bids_volume, provider=self
        )
    # end bid_volume

    def ask_volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.asks_volume, provider=self
        )
    # end ask_volume

    def data(self) -> SymbolsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        datasets: Dict[str, Dict[str, Dict[dt.datetime, Dict[str, float]]]] = {}

        for key, data in zip(
            (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME),
            (self.bids, self.asks, self.bids_volume, self.asks_volume)
        ):
            for exchange, symbols in data.items():
                for symbol, prices in symbols.items():
                    for i, (time, price) in enumerate(prices):
                        try:
                            if isinstance(time, str):
                                time = dt.datetime.fromisoformat(time)

                            elif isinstance(time, int):
                                time = dt.datetime.fromtimestamp(time)

                        except (Type, ValueError):
                            pass
                        # end try

                        (
                            datasets.
                            setdefault(exchange, {}).
                            setdefault(symbol, {}).
                            setdefault(time, {})
                        )[key] = price
                    # end for
                # end for
            # end for
        # end for

        new_datasets: SymbolsMarketData = {}

        for exchange, symbols in datasets.items():
            for symbol, prices in symbols.copy().items():
                new_datasets.setdefault(exchange, {})[symbol] = sorted(
                    list(prices.items()), key=lambda pair: pair[0]
                )
            # end for
        # end for

        return new_datasets
    # end data

    def datasets(self) -> SymbolsMarketDatasets:
        """
        Rebuilds the dataset from the market state.

        :return: The dataset of the state data.
        """

        datasets: SymbolsMarketDatasets = {}

        for exchange, symbols in self.data().items():
            for symbol, rows in symbols.items():
                dataset = create_orderbook_dataframe()

                for time, row in rows:
                    dataset.loc[time] = row
                # end for
            # end for
        # end for

        return datasets
# end symbols_market_state_to_datasets
# end SymbolsMarketStates

def symbols_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    bids: SymbolsPrices = {}
    asks: SymbolsPrices = {}
    bids_volume: SymbolsPrices = {}
    asks_volume: SymbolsPrices = {}

    if (length is None) and (not adjust):
        length = min([len(screener.market) for screener in screeners])
    # end if

    for screener in screeners:
        if adjust and (length is None):
            length = len(screener.market)

        elif adjust:
            length = min([len(screener.market), length])
        # end if

        if length > len(screener.market):
            raise ValueError(
                f"Data of '{screener.exchange}' symbol in '{screener.symbol}' exchange "
                f"is not long enough for the requested length: {length}. "
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end if

        for key, data in zip(
            (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME),
            (bids, asks, bids_volume, asks_volume)
        ):
            (
                data.
                setdefault(screener.exchange, {}).
                setdefault(
                    screener.symbol,
                    list(
                        zip(
                            list(screener.market.index[-length:]),
                            list(screener.market[key][-length:])
                        )
                    )
                )
            )
        # end for
    # end for

    return SymbolsMarketState(
        screeners=screeners, bids=bids, asks=asks,
        bids_volume=bids_volume, asks_volume=asks_volume
    )
# end symbols_market_state

def merge_symbols_market_states(
        *states: SymbolsMarketState, sort: Optional[bool] = True
) -> SymbolsMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the prices by the time.

    :return: The states object.
    """

    bids: SymbolsPrices = {}
    asks: SymbolsPrices = {}
    bids_volume: SymbolsPrices = {}
    asks_volume: SymbolsPrices = {}

    for state in states:
        for key, (state_data, data) in zip(
            (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME),
            (
                (state.bids, bids),
                (state.asks, asks),
                (state.bids_volume, bids_volume),
                (state.asks_volume, asks_volume)
            )
        ):
            for exchange, symbols in state_data.items():
                for symbol, prices in symbols.items():
                    (
                        data.setdefault(exchange, {}).
                        setdefault(symbol, []).
                        extend(prices)
                    )
                # end for
            # end for
        # end for
    # end for

    screeners = []

    if sort:
        for prices_data in (bids, asks, bids_volume, asks_volume):
            for exchange, symbols in prices_data.items():
                for symbol, prices in symbols.items():
                    prices.sort(key=lambda pair: pair[0])
                # end for
            # end for
        # end for
    # end if

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return SymbolsMarketState(
        screeners=set(screeners), bids=bids, asks=asks,
        bids_volume=bids_volume, asks_volume=asks_volume
    )
# end merge_symbols_market_states

def merge_assets_market_states(
        *states: AssetsMarketState, sort: Optional[bool] = True
) -> AssetsMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the prices by the time.

    :return: The states object.
    """

    bids: AssetsPrices = {}
    asks: AssetsPrices = {}
    bids_volume: AssetsPrices = {}
    asks_volume: AssetsPrices = {}

    for state in states:
        for key, (state_data, data) in zip(
            (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME),
            (
                (state.bids, bids),
                (state.asks, asks),
                (state.bids_volume, bids_volume),
                (state.asks_volume, asks_volume)
            )
        ):
            for exchange, symbols in state_data.items():
                for base, quotes in symbols.items():
                    for quote, prices in quotes.items():
                        (
                            data.setdefault(exchange, {}).
                            setdefault(base, {}).
                            setdefault(quote, []).
                            extend(prices)
                        )
                # end for
            # end for
        # end for
    # end for

    if sort:
        for prices_data in (bids, asks, bids_volume, asks_volume):
            for exchange, bases in prices_data.items():
                for base, quotes in bases.items():
                    for quote, prices in quotes.items():
                        prices.sort(key=lambda pair: pair[0])
                    # end for
                # end for
            # end for
        # end for
    # end if

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return AssetsMarketState(
        screeners=set(screeners), bids=bids, asks=asks,
        bids_volume=bids_volume, asks_volume=asks_volume
    )
# end merge_assets_market_states

def merge_symbols_market_data(
        *data: SymbolsMarketData, sort: Optional[bool] = True
) -> SymbolsMarketData:
    """
    Concatenates the states of the market.

    :param data: The states to concatenate.
    :param sort: The value to sort the prices by the time.

    :return: The states object.
    """

    new_data: SymbolsMarketData = {}

    for data_packet in data:
        for exchange, symbols in data_packet.items():
            for symbol, prices in symbols.items():
                (
                    new_data.setdefault(exchange, {}).
                    setdefault(symbol, []).
                    extend(prices)
                )
            # end for
        # end for
    # end for

    if sort:
        for exchange, symbols in new_data.items():
            for symbol, prices in symbols.items():
                prices.sort(key=lambda pair: pair[0])
            # end for
        # end for
    # end if

    return new_data
# end merge_symbols_market_states

def merge_assets_market_data(
        *data: AssetsMarketData, sort: Optional[bool] = True
) -> AssetsMarketData:
    """
    Concatenates the states of the market.

    :param data: The states to concatenate.
    :param sort: The value to sort the prices by the time.

    :return: The states object.
    """

    new_data: AssetsMarketData = {}

    for data_packet in data:
        for exchange, bases in data_packet.items():
            for base, quotes in bases.items():
                for quote, prices in quotes.items():
                    (
                        new_data.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, []).
                        extend(prices)
                    )
                # end for
        # end for
    # end for

    if sort:
        for exchange, bases in new_data.items():
            for base, quotes in bases.items():
                for quote, prices in quotes.items():
                    prices.sort(key=lambda pair: pair[0])
                # end for
            # end for
        # end for
    # end if

    return new_data
# end merge_assets_market_states

def symbols_market_dataset_to_assets_market_datasets(
        datasets: SymbolsMarketDatasets, separator: Optional[str] = None
) -> AssetsMarketDatasets:
    """
    Converts the datasets structure from symbols to assets.

    :param datasets: The datasets to convert.
    :param separator: The separator for the symbols.

    :return: The result structure.
    """

    assets_datasets: AssetsMarketDatasets = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)
            (
                assets_datasets.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, dataset)
            )
        # end for
    # end for

    return assets_datasets
# end symbols_market_dataset_to_assets_market_datasets

def assets_market_dataset_to_symbols_market_datasets(
        datasets: AssetsMarketDatasets, separator: Optional[str] = None
) -> SymbolsMarketDatasets:
    """
    Converts the datasets structure from assets to symbols.

    :param datasets: The datasets to convert.
    :param separator: The separator for the symbols.

    :return: The result structure.
    """

    symbols_datasets: SymbolsMarketDatasets = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, dataset in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)
                (
                    symbols_datasets.
                    setdefault(exchange, {}).
                    setdefault(symbol, dataset)
                )
        # end for
    # end for

    return symbols_datasets
# end assets_market_dataset_to_symbols_market_datasets

def assets_market_prices_to_symbol_market_prices(
        prices: AssetsPrices, separator: Optional[str] = None
) -> SymbolsPrices:
    """
    Converts an assets market prices into a symbols market prices.

    :param prices: The source prices.
    :param separator: The separator for the symbols.

    :return: The result prices.
    """

    symbols_prices: SymbolsPrices = {}

    for exchange, bases in prices.items():
        for base, quotes in bases.items():
            for quote, data in quotes.items():
                for time, price in data:
                    (
                        symbols_prices.
                        setdefault(exchange, {}).
                        setdefault(
                            parts_to_symbol(base, quote, separator=separator)
                        )
                    ).append((time, price))
                # end for
            # end for
        # end for
    # end for

    return symbols_prices
# end assets_market_prices_to_symbol_market_prices

def assets_market_state_to_symbols_market_state(
        state: AssetsMarketState,
        separator: Optional[str] = None
) -> SymbolsMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsMarketState(
        bids=assets_market_prices_to_symbol_market_prices(
            state.bids, separator=separator
        ),
        asks=assets_market_prices_to_symbol_market_prices(
            state.asks, separator=separator
        ),
        bids_volume=assets_market_prices_to_symbol_market_prices(
            state.bids_volume, separator=separator
        ),
        asks_volume=assets_market_prices_to_symbol_market_prices(
            state.asks_volume, separator=separator
        )
    )
# end assets_market_state_to_symbols_market_state

def symbol_market_prices_to_assets_market_prices(
        prices: SymbolsPrices, separator: Optional[str] = None
) -> AssetsPrices:
    """
    Converts a symbols market prices into an assets market prices.

    :param prices: The source prices.
    :param separator: The separator for the symbols.

    :return: The result prices.
    """

    assets_prices: AssetsPrices = {}

    for exchange, symbols in prices.items():
        for symbol, data in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)

            for time, price in data:
                (
                    assets_prices.
                    setdefault(exchange, {}).
                    setdefault(base, {}).
                    setdefault(quote, [])
                ).append((time, price))
            # end for
        # end for
    # end for

    return assets_prices
# end symbol_market_prices_to_assets_market_prices

def symbols_market_state_to_assets_market_state(
        state: SymbolsMarketState,
        separator: Optional[str] = None
) -> AssetsMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsMarketState(
        bids=symbol_market_prices_to_assets_market_prices(
            state.bids, separator=separator
        ),
        asks=symbol_market_prices_to_assets_market_prices(
            state.asks, separator=separator
        ),
        bids_volume=symbol_market_prices_to_assets_market_prices(
            state.bids_volume, separator=separator
        ),
        asks_volume=symbol_market_prices_to_assets_market_prices(
            state.asks_volume, separator=separator
        )
    )
# end symbols_market_state_to_assets_market_state

def assets_market_data_to_symbols_market_data(
        data: AssetsMarketData,
        separator: Optional[str] = None
) -> SymbolsMarketData:
    """
    Converts the structure of the market data from assets to symbols.

    :param data: The data to convert.
    :param separator: The separator for the symbols.

    :return: The data in the new structure
    """

    symbols_data: SymbolsMarketData = {}

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote, data in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                (
                    symbols_data.
                    setdefault(exchange, {}).
                    setdefault(symbol, data)
                )
            # end for
    # end for

    return symbols_data
# end assets_market_data_to_symbols_market_data

def symbols_market_data_to_assets_market_data(
        data: SymbolsMarketData,
        separator: Optional[str] = None
) -> AssetsMarketData:
    """
    Converts the structure of the market data from assets to symbols.

    :param data: The data to convert.
    :param separator: The separator for the symbols.

    :return: The data in the new structure
    """

    assets_data: AssetsMarketData = {}

    for exchange, symbols in data.items():
        for symbol, data in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)

            (
                assets_data.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, data)
            )
            # end for
        # end for
    # end for

    return assets_data
# end assets_market_data_to_symbols_market_data

_ST = TypeVar("_ST", Type[BaseScreener], Type[OrderbookScreener])

AssetsScreeners = Dict[str, Dict[str, Dict[str, Union[BaseScreener, _ST]]]]

def assets_market_datasets_to_assets_screeners(
        datasets: AssetsMarketDatasets,
        base: Optional[_ST] = None,
        screeners: Optional[BaseScreener] = None,
        separator: Optional[str] = None
) -> AssetsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.
    :param separator: The separator for the symbols.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []
    # end if

    screener_base = base or OrderbookScreener

    new_screeners: AssetsScreeners = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, dataset in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)
                for screener in screeners:
                    if not (
                        (screener.exchange.lower() == exchange.lower()) and
                        (screener.symbol.lower() == symbol.lower())
                    ):
                        screener = screener_base(
                            symbol=symbol, exchange=exchange, market=dataset
                        )

                    else:
                        screener.market = dataset
                    # end if

                    (
                        new_screeners.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, screener)
                    )
                # end for
            # end for
        # end for
    # end for

    return new_screeners
# end assets_market_datasets_to_assets_screeners

SymbolsScreeners = Dict[str, Dict[str, Union[BaseScreener, _ST]]]

def symbols_market_datasets_to_symbols_screeners(
        datasets: SymbolsMarketDatasets,
        base: Optional[_ST] = None,
        screeners: Optional[BaseScreener] = None
) -> SymbolsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []
    # end if

    screener_base = base or OrderbookScreener

    new_screeners: SymbolsScreeners = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            for screener in screeners:
                if not (
                    (screener.exchange.lower() == exchange.lower()) and
                    (screener.symbol.lower() == symbol.lower())
                ):
                    screener = screener_base(
                        symbol=symbol, exchange=exchange, market=dataset
                    )

                else:
                    screener.market = dataset
                # end if

                (
                    new_screeners.setdefault(exchange, {}).
                    setdefault(symbol, screener)
                )
            # end for
        # end for
    # end for

    return new_screeners
# end symbols_market_datasets_to_symbols_screeners

def assets_screeners(screeners: AssetsScreeners) -> List[Union[BaseScreener, _ST]]:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.

    :return: The screeners' collection.
    """

    screeners_collection = []

    for exchange, bases in screeners.items():
        for base, quotes in bases.items():
            for quote, screener in quotes.items():
                screeners_collection.append(screener)
            # end for
        # end for
    # end for

    return screeners_collection
# end assets_screeners

def symbols_screeners(screeners: SymbolsScreeners) -> List[Union[BaseScreener, _ST]]:
    """
    Collects the screeners from the symbols screeners structure.

    :param screeners: The screeners structure.

    :return: The screeners' collection.
    """

    screeners_collection = []

    for exchange, symbols in screeners.items():
        for symbol, screener in symbols.items():
            screeners_collection.append(screener)
        # end for
    # end for

    return screeners_collection
# end symbols_screeners

def add_symbols_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: SymbolsMarketData,
        adjust: Optional[bool] = True
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    """

    for exchange, symbols in data.items():
        for symbol, rows in symbols.items():
            found_screeners = find_screeners(
                screeners, exchange=exchange, symbol=symbol
            )

            if not found_screeners and not adjust:
                raise ValueError(
                    f"Unable to find a screener with exchange "
                    f"'{exchange}' and symbol '{symbol}' to update its data. "
                    f"Consider setting the 'adjust' parameter to True, ignore."
                )
            # end if

            screener = found_screeners[0]

            for time, row in rows:
                screener.market.loc[time] = row
            # end for
        # end for
    # end for
# end add_symbols_data_to_screeners

def add_assets_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: AssetsMarketData,
        adjust: Optional[bool] = True
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    """

    return add_symbols_data_to_screeners(
        screeners=screeners,
        data=assets_market_data_to_symbols_market_data(data=data),
        adjust=adjust
    )
# end add_assets_data_to_screeners