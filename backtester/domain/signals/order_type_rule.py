"""
Order Type Rule Entity
"""
from copy import deepcopy

import pandas as pd

from modules.strategy_service.api.requests.trading_system_rules import \
    OrderTypeRules
from modules.strategy_service.enums_shared.order_type import OrderType

from .group_rule import GroupRule
from .indicator_registry import IndicatorRegistry
from .signals import Signals


class OrderTypeRule:
    """
    Represents an order type rule within a trading system.
    """

    def __init__(
            self,
            signal_indexes: pd.Series,
            order_type: OrderType,
            order_type_rules: OrderTypeRules,
            customer_id: str,
            trading_system_rule_id: str,
            indicator_registry: IndicatorRegistry
    ):
        """
        Initializes an OrderTypeRule instance.
        :param signal_indexes: pd.Series with signals
        :param order_type: OrderType, indicating the type of order (BUY/SELL)
        :param order_type_rules: OrderTypeRules, containing rules for the order type
        :param customer_id: ID of the customer
        :param trading_system_rule_id: ID of the trading system rule
        :param indicator_registry: IndicatorRegistry instance to manage indicators
        """
        self.customer_id = customer_id
        self.trading_system_rule_id = trading_system_rule_id
        self.order_type_rule_id = order_type_rules.order_type_rule_id
        self.signal_indexes: pd.Series = signal_indexes
        self.order_type: OrderType = order_type
        self.order_type_rules: OrderTypeRules = order_type_rules
        self.signals: Signals = Signals(
            signal_indexes=deepcopy(~signal_indexes),
            order_type=self.order_type
        )
        self.group_rules = []
        self.rules = []
        if len(order_type_rules.group_rules) > 0:
            self.group_rules = [
                GroupRule(
                    signal_indexes=deepcopy(signal_indexes),
                    order_type=self.order_type,
                    rule_properties=self.order_type_rules.group_rules.get(key).rules,
                    group_rule_id=self.order_type_rules.group_rules.get(key).group_rule_id,
                    customer_id=self.customer_id,
                    order_type_rule_id=self.order_type_rule_id,
                    indicator_registry=indicator_registry
                ) for key in self.order_type_rules.group_rules.keys()
            ]
            for group_rule in self.group_rules:
                self.rules += group_rule.rules

    def __len__(self) -> int:
        """
        Returns the number of rules in the order type rule.
        """
        return len(self.rules)

    def __repr__(self) -> str:
        """
        Returns a string representation of the OrderTypeRule instance.
        """
        return (f"OrderTypeRule(order_type_rule_id={self.order_type_rule_id},"
                f" customer_id={self.customer_id},"
                f" order_type={self.order_type})")
