"""
Signals class to hold signal indexes and their order type.
"""
from copy import deepcopy

import pandas as pd

from backtester.domain.enums.order_type import OrderType


class Signals:
    """
    Signals class represents a collection of trading signals.
    """

    def __init__(
            self,
            signal_indexes: pd.Series,
            order_type: OrderType
    ):
        """
        Initializes a Signals instance.
        :param signal_indexes: pd.Series with signal indexes,
         where True indicates a signal is present
        :param order_type: OrderType, indicating the type of order (BUY/SELL/NO_ACTION)
        """
        self.signal_indexes = deepcopy(signal_indexes)
        self.order_type = order_type

    def inner_merge(self, signal_indexes: pd.Series) -> None:
        """
        Adds two series with signal indexes together, using the AND operator
        :param signal_indexes: the signal indexes to be added
        """
        self.signal_indexes &= signal_indexes

    def outer_merge(self, signal_indexes: pd.Series) -> None:
        """
        Adds two series with signal indexes together, using the OR operator
        :param signal_indexes: the signal indexes to be added
        """
        self.signal_indexes |= signal_indexes

    def __repr__(self) -> str:
        """
        Returns a string representation of the Signals instance.
        """
        return f"Signals(order_type={self.order_type})"
