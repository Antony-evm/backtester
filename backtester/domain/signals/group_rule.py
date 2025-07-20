"""
Group Rule
"""
from copy import deepcopy
from typing import Dict

import pandas as pd


from .indicator_registry import IndicatorRegistry
from .rule import Rule
from .signals import Signals
from backtester.domain.enums.order_type import OrderType
from backtester.api.requests.trading_system import RuleProperties


class GroupRule:
    """
    Group signal is a higher signal structure than the block signal,
     but less than the strategy signal.
    Each block belongs to a group, defined by its group id.
    Signals between blocks should be combined using the OR operator,
     if they belong to the same group
    """

    def __init__(
            self,
            signal_indexes: pd.Series,
            order_type: OrderType,
            rule_properties: Dict[str, RuleProperties],
            group_rule_id: str,
            order_type_rule_id: str,
            indicator_registry: IndicatorRegistry
    ):
        """
        Initializes a GroupRule instance.
        :param signal_indexes: pd.Series with signals
        :param order_type: OrderType, indicating the type of order (BUY/SELL)
        :param rule_properties: Properties of the rules
        :param group_rule_id: ID of the group rule
        :param order_type_rule_id: ID of the order type rule
        :param indicator_registry: IndicatorRegistry instance to manage indicators
        """
        self.order_type_rule_id = order_type_rule_id
        self.group_rule_id = group_rule_id
        self.signal_indexes: pd.Series = signal_indexes
        self.order_type: OrderType = order_type
        self.rule_properties = rule_properties

        self.signals: Signals = Signals(
            signal_indexes=deepcopy(signal_indexes),
            order_type=self.order_type
        )
        self.rules = [
            Rule(
                signal_indexes=deepcopy(signal_indexes),
                order_type=self.order_type,
                rule_properties=self.rule_properties.get(key),
                group_rule_id=self.group_rule_id,
                indicator_registry=indicator_registry
            ) for key in self.rule_properties.keys()
        ]

    def __len__(self) -> int:
        """
        Returns the number of rules in the group rule.
        """
        return len(self.rules)

    def __repr__(self) -> str:
        """
        Returns a string representation of the GroupRule instance.
        """
        return (f"GroupRule(group_rule_id={self.group_rule_id},"
                f" order_type={self.order_type})")
