"""
Order Type Enum
"""
from enum import Enum


class OrderType(Enum):
    """
    Enum representing the type of order in a trading strategy.
    """
    BUY = 'BUY'
    SELL = 'SELL'
    NO_ACTION = 'NO_ACTION'

    @property
    def opposite(self):
        """
        Returns the opposite of the current order type using a mapping dictionary.
        """
        opposites = {
            OrderType.BUY: OrderType.SELL,
            OrderType.SELL: OrderType.BUY,
            OrderType.NO_ACTION: OrderType.NO_ACTION
        }
        return opposites[self]
