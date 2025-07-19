"""
Trade Result Enum
"""
from enum import Enum


class TradeResult(Enum):
    """
    Enum representing the result of a trade.
    """
    WIN = 'WIN'
    LOSS = 'LOSS'
    UNDETERMINED = 'UNDETERMINED'

    @property
    def actionable(self) -> bool:
        """
        Determines if the trade result is actionable.
        :return: True if the result is actionable (WIN or LOSS),
         False otherwise (UNDETERMINED).
        """
        actions = {
            TradeResult.WIN: True,
            TradeResult.LOSS: True,
            TradeResult.UNDETERMINED: False
        }
        return actions[self]
