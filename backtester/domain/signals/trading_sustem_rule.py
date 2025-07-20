"""
Trading System Rule Entity
"""
from copy import deepcopy

import pandas as pd


from .indicator_registry import IndicatorRegistry
from .order_type_rule import OrderTypeRule
from .signals import Signals
from backtester.api.requests.trading_system import TradingSystemRules
from backtester.domain.enums.order_type import OrderType


class TradingSystemRule:
    """
    Represents the highest form of signals.
    Handles the aggregation and updating of signals for a given trading strategy.
    """

    def __init__(
            self,
            signal_indexes: pd.Series,
            trading_system_rules: TradingSystemRules,
            trading_system_rule_id: str,
            indicator_registry: IndicatorRegistry
    ):
        """
        Initializes a TradingSystemRule instance.
        :param signal_indexes: pd.Series with signal indexes,
        :param trading_system_rules: TradingSystemRules,
         containing rules for the trading system
        :param trading_system_rule_id: id of the trading system rule
        :param customer_id: ID of the customer
        :param indicator_registry: IndicatorRegistry instance to manage indicators
        """
        self.trading_system_rule_id = trading_system_rule_id
        self.signal_indexes = signal_indexes
        self.base_signals = Signals(
            signal_indexes=deepcopy(signal_indexes),
            order_type=OrderType.NO_ACTION
        )
        self.buy_rules = OrderTypeRule(
            signal_indexes=deepcopy(signal_indexes),
            order_type=OrderType.BUY,
            order_type_rules=trading_system_rules.root.get(OrderType.BUY),
            trading_system_rule_id=self.trading_system_rule_id,
            indicator_registry=indicator_registry
        )

        self.sell_rules = OrderTypeRule(
            signal_indexes=deepcopy(signal_indexes),
            order_type=OrderType.SELL,
            order_type_rules=trading_system_rules.root.get(OrderType.SELL),
            trading_system_rule_id=self.trading_system_rule_id,
            indicator_registry=indicator_registry
        )
        self.group_rules = self.buy_rules.group_rules + self.sell_rules.group_rules
        self.block_rules = self.buy_rules.rules + self.sell_rules.rules

    def __repr__(self) -> str:
        """
        Returns a string representation of the TradingSystemRule instance.
        """
        return (f"TradingSystemRule("
                f"trading_system_rule_id={self.trading_system_rule_id}")
