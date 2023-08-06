# market.py

from abc import ABCMeta
from typing import (
    Iterable, Dict, Optional, Union,
    Any, ClassVar, List
)

from attrs import define

from represent import represent, Modifiers

import numpy as np

from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.dataset import BIDS, ASKS
from crypto_screening.symbols import symbol_to_parts

__all__ = [
    "assets_market_state",
    "AssetsMarketState",
    "validate_assets_market_state_prices_symbol",
    "assets_market_state",
    "assets_market_price",
    "is_symbol_in_assets_market_prices",
    "SymbolsMarketState",
    "symbols_market_state",
    "symbols_market_price_sequence",
    "symbols_market_states",
    "symbols_market_price",
    "merge_assets_market_states",
    "merge_symbols_market_states",
    "assets_market_price_sequence",
    "validate_symbols_market_state_prices_symbol",
    "assets_market_states",
    "AssetsMarketStates",
    "SymbolsMarketStates",
    "is_exchange_in_market_prices",
    "is_symbol_in_symbols_market_prices"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, float]]]
SymbolsPrices = Dict[str, Dict[str, float]]
AssetsPricesSequence = Dict[str, Dict[str, Dict[str, List[float]]]]
SymbolsPricesSequence = Dict[str, Dict[str, List[float]]]

def is_exchange_in_market_prices(
        exchange: str,
        prices: Union[
            AssetsPrices, AssetsPricesSequence,
            SymbolsPrices, SymbolsPricesSequence
        ]
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
        prices: Union[AssetsPrices, AssetsPricesSequence],
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
        prices: Union[SymbolsPrices, SymbolsPricesSequence]
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
        prices: Union[AssetsPrices, AssetsPricesSequence],
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
        prices: Union[SymbolsPrices, SymbolsPricesSequence],
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
) -> float:
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

    return float(prices[exchange][base][quote])
# end assets_market_price

def symbols_market_price(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> float:
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

    return float(prices[exchange][symbol])
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

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
    """

    bids: AssetsPrices
    asks: AssetsPrices

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **AssetsMarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks"])

    def bid(self, exchange: str, symbol: str, separator: Optional[str] = None) -> float:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_price(
            exchange=exchange, symbol=symbol, prices=self.bids,
            separator=separator, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str, separator: Optional[str] = None) -> float:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_price(
            exchange=exchange, symbol=symbol, prices=self.asks,
            separator=separator, provider=self
        )
    # end ask
# end MarketState

def assets_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        adjust: Optional[bool] = True
) -> AssetsMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    bids: AssetsPrices = {}
    asks: AssetsPrices = {}

    for screener in screeners:
        base, quote = symbol_to_parts(
            symbol=screener.symbol, separator=separator
        )

        if adjust and (len(screener.market) == 0):
            continue
        # end if

        try:
            (
                bids.
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(quote, screener.market[BIDS][-1])
            )
            (
                asks.
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(quote, screener.market[ASKS][-1])
            )

        except IndexError:
            raise ValueError(
                f"Data of '{screener.exchange}' symbol in "
                f"'{screener.symbol}' exchange is empty."
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end try
    # end for

    return AssetsMarketState(
        screeners=screeners, bids=bids, asks=asks
    )
# end assets_market_state

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

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
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

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
    """

    bids: SymbolsPrices
    asks: SymbolsPrices

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **SymbolsMarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks"])

    def bid(self, exchange: str, symbol: str) -> float:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_price(
            exchange=exchange, symbol=symbol,
            prices=self.bids, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str) -> float:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_price(
            exchange=exchange, symbol=symbol,
            prices=self.asks, provider=self
        )
    # end ask
# end SymbolsMarketState

def symbols_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        adjust: Optional[bool] = True
) -> SymbolsMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    bids: SymbolsPrices = {}
    asks: SymbolsPrices = {}

    for screener in screeners:
        if adjust and (len(screener.market) == 0):
            continue
        # end if

        try:
            (
                bids.
                setdefault(screener.exchange, {}).
                setdefault(screener.symbol, screener.market[BIDS][-1])
            )
            (
                asks.
                setdefault(screener.exchange, {}).
                setdefault(screener.symbol, screener.market[ASKS][-1])
            )

        except IndexError:
            raise ValueError(
                f"Data of '{screener.exchange}' symbol in "
                f"'{screener.symbol}' exchange is empty."
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end try
    # end for

    return SymbolsMarketState(
        screeners=screeners, bids=bids, asks=asks
    )
# end symbols_market_state

def symbols_market_price_sequence(
        exchange: str,
        symbol: str,
        prices: SymbolsPricesSequence,
        provider: Optional[Any] = None
) -> List[float]:
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

    return [float(value) for value in prices[exchange][symbol]]
# end symbols_market_price_sequence

@define(repr=False)
@represent
class AssetsMarketStates(AssetsMarketBase):
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

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
    """

    bids: AssetsPricesSequence
    asks: AssetsPricesSequence

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **AssetsMarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks"])

    def bid(self, exchange: str, symbol: str, separator: Optional[str] = None) -> List[float]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_price_sequence(
            exchange=exchange, symbol=symbol, prices=self.bids,
            separator=separator, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str, separator: Optional[str] = None) -> List[float]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_price_sequence(
            exchange=exchange, symbol=symbol, prices=self.asks,
            separator=separator, provider=self
        )
    # end ask
# end AssetsMarketStates

def assets_market_price_sequence(
        exchange: str,
        symbol: str,
        prices: AssetsPricesSequence,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> List[float]:
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

    return [float(value) for value in prices[exchange][base][quote]]
# end assets_market_price_sequence

def assets_market_states(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsMarketStates:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    bids: AssetsPricesSequence = {}
    asks: AssetsPricesSequence = {}

    if (length is None) and (not adjust):
        length = min([len(screener.market) for screener in screeners])
    # end if

    for screener in screeners:
        if adjust and (length is None):
            length = len(screener.market)

        elif adjust:
            length = min([len(screener.market), length])
        # end if

        base, quote = symbol_to_parts(
            symbol=screener.symbol, separator=separator
        )

        try:
            (
                bids.
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(quote, list(screener.market[BIDS][-length:]))
            )
            (
                asks.
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(quote, list(screener.market[ASKS][-length:]))
            )

        except IndexError:
            raise ValueError(
                f"Data of '{screener.exchange}' "
                f"symbol in '{screener.symbol}' exchange "
                f"is not long enough for the requested length: {length}. "
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end try
    # end for

    return AssetsMarketStates(
        screeners=screeners, bids=bids, asks=asks
    )
# end assets_market_state

@define(repr=False)
@represent
class SymbolsMarketStates(SymbolsMarketBase):
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

    >>> from crypto_screening.collect.market import AssetsMarketState
    >>>
    >>> state = assets_market_state(["BTC", "ETH", "LTC"], currency="USDT")
    """

    bids: SymbolsPricesSequence
    asks: SymbolsPricesSequence

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **AssetsMarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks"])

    def bid(self, exchange: str, symbol: str) -> List[float]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_price_sequence(
            exchange=exchange, symbol=symbol,
            prices=self.bids, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str) -> List[float]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_price_sequence(
            exchange=exchange, symbol=symbol,
            prices=self.asks, provider=self
        )
    # end ask
# end SymbolsMarketStates

def symbols_market_states(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsMarketStates:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    bids: SymbolsPricesSequence = {}
    asks: SymbolsPricesSequence = {}

    if (length is None) and (not adjust):
        length = min([len(screener.market) for screener in screeners])
    # end if

    for screener in screeners:
        if adjust and (length is None):
            length = len(screener.market)

        elif adjust:
            length = min([len(screener.market), length])
        # end if

        try:
            (
                bids.
                setdefault(screener.exchange, {}).
                setdefault(
                    screener.symbol,
                    list(screener.market[BIDS][-length:])
                )
            )
            (
                asks.
                setdefault(screener.exchange, {}).
                setdefault(
                    screener.symbol,
                    list(screener.market[ASKS][-length:])
                )
            )

        except IndexError:
            raise ValueError(
                f"Data of '{screener.exchange}' symbol in '{screener.symbol}' exchange "
                f"is not long enough for the requested length: {length}. "
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end try
    # end for

    return SymbolsMarketStates(
        screeners=screeners, bids=bids, asks=asks
    )
# end symbols_market_states

def merge_symbols_market_states(*states: SymbolsMarketState) -> SymbolsMarketStates:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.

    :return: The states object.
    """

    bids: SymbolsPricesSequence = {}
    asks: SymbolsPricesSequence = {}

    for state in states:
        for exchange, symbols in state.bids.items():
            for symbol, price in symbols.items():
                (
                    bids.setdefault(exchange, {}).
                    setdefault(symbol, []).
                    append(price)
                )
            # end for
        # end for
    # end for

    for state in states:
        for exchange, symbols in state.asks.items():
            for symbol, price in symbols.items():
                (
                    asks.setdefault(exchange, {}).
                    setdefault(symbol, []).
                    append(price)
                )
            # end for
        # end for
    # end for

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return SymbolsMarketStates(
        screeners=set(screeners), bids=bids, asks=asks
    )
# end merge_symbols_market_states

def merge_assets_market_states(*states: AssetsMarketState) -> AssetsMarketStates:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.

    :return: The states object.
    """

    bids: AssetsPricesSequence = {}
    asks: AssetsPricesSequence = {}

    for state in states:
        for exchange, symbols in state.bids.items():
            for base, quotes in symbols.items():
                for quote, price in quotes.items():
                    (
                        bids.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, []).
                        append(price)
                    )
            # end for
        # end for
    # end for

    for state in states:
        for exchange, symbols in state.asks.items():
            for base, quotes in symbols.items():
                for quote, price in quotes.items():
                    (
                        asks.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, []).
                        append(price)
                    )
            # end for
        # end for
    # end for

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return AssetsMarketStates(
        screeners=set(screeners), bids=bids, asks=asks
    )
# end merge_assets_market_states