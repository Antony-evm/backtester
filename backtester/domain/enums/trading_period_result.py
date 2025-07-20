"""
TradingPeriodResult Enum
"""
from enum import Enum


class TradingPeriodResult(Enum):
    """
    Enum representing the result of a trading period.
    """
    LOWER_LIMIT = 'LOWER_LIMIT'
    HIGHER_LIMIT = 'HIGHER_LIMIT'
    OPPOSING_TRADE = 'OPPOSING_TRADE'
    CONTINUE_TRADE = 'CONTINUE_TRADE'

    @property
    def end_trade(self) -> bool:
        """
        Determines if the trading period result indicates the end of a trade.
        :return: True if the result indicates the end of a trade, False otherwise.
        """
        results = {
            TradingPeriodResult.LOWER_LIMIT: True,
            TradingPeriodResult.HIGHER_LIMIT: True,
            TradingPeriodResult.OPPOSING_TRADE: True,
            TradingPeriodResult.CONTINUE_TRADE: False,

        }
        return results[self]
