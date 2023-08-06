# dynamic.py

from typing import Optional, Iterable, List, Union, Dict

from represent import Modifiers

import pandas as pd

from crypto_screening.collect.screeners import exchanges_symbols_screeners
from crypto_screening.collect.assets import exchanges_symbols_quote_assets
from crypto_screening.collect.market import (
    symbols_market_state, assets_market_state,
    SymbolsMarketState, AssetsMarketState,
    assets_market_state, symbols_market_state,
    SymbolsMarketState, AssetsMarketState
)
from crypto_screening.market.screeners.container import ScreenersContainer
from crypto_screening.market.screeners import BaseScreener

__all__ = [
    "DynamicScreener"
]

class DynamicScreener(ScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    - data:
        The structure of the screeners, by exchanges and symbols.

    >>> from crypto_screening.market.dynamic import DynamicScreener
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> dynamic_screener = DynamicScreener(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> dynamic_screener.find_screener(exchange="binance", symbol="BTC/USDT"))
    >>> dynamic_screener.data(exchange="binance", symbol="BTC/USDT", length=10))
    """

    __modifiers__ = Modifiers(**ScreenersContainer.__modifiers__)
    __modifiers__.hidden.extend(["currencies", "exchanges"])
    __modifiers__.excluded.append("exchanges")

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        super().__init__(screeners=screeners)

        self.currencies = exchanges_symbols_quote_assets(data=self.market)
        self.exchanges = list(self.market.keys())
    # end __init__

    def find_dataset(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screener = self.find_screener(exchange=exchange, symbol=symbol)

        length = min(length or 0, len(screener.market))

        return screener.market.iloc[-length:]
    # end find_dataset

    def find_datasets(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> List[pd.DataFrame]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screeners = self.find_screeners(exchange=exchange, symbol=symbol)

        return [
            screener.market.iloc[-min(length or 0, len(screener.market)):]
            for screener in screeners
        ]
    # end find_dataset

    def symbols_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            adjust: Optional[bool] = True,
            separator: Optional[str] = None,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsMarketState:
        """
        Fetches the prices and relations between the assets.

        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_market_state(screeners=screeners)
    # end symbols_market_state

    def assets_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            adjust: Optional[bool] = True,
            separator: Optional[str] = None,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsMarketState:
        """
        Fetches the prices and relations between the assets.

        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_market_state(screeners=screeners, separator=separator)
    # end assets_market_state

    def assets_market_states(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsMarketState:
        """
        Fetches the prices and relations between the assets.

        :param length: The length of the prices.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_market_state

    def symbols_market_states(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsMarketState:
        """
        Fetches the prices and relations between the assets.

        :param length: The length of the prices.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = exchanges_symbols_screeners(
            screeners=self.screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_market_state
# end DynamicScreener