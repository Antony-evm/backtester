"""
Rule class represents a trading rule in a strategy.
"""
from copy import deepcopy

import pandas as pd


from .indicator_registry import IndicatorRegistry
from .signals import Signals
from .tile import Tile
from backtester.domain.enums.order_type import OrderType
from backtester.domain.enums.rule_comparison_method import RuleComparisonMethod
from backtester.domain.enums.rule_property_type import RulePropertyType
from backtester.api.requests.trading_system import RuleProperties


class Rule:
    """
    Block signals represents the signals of a strategy block.
    It represents the most basic signal structure
    It has a distinct order type, BUY or SELL
    """

    def __init__(
            self,
            signal_indexes: pd.Series,
            order_type: OrderType,
            rule_properties: RuleProperties,
            group_rule_id: str,
            indicator_registry: IndicatorRegistry
    ):
        """
        Initializes a Rule instance.
        """
        self.group_rule_id = group_rule_id
        self.rule_id = rule_properties.rule_id
        self.signal_indexes = signal_indexes
        self.order_type = order_type
        self.indicator_registry = indicator_registry
        self.first_tile: Tile = Tile(
            rule_property=rule_properties.first_property,
            rule_id=self.rule_id
        )
        if self.first_tile.type == RulePropertyType.INDICATOR:
            self.indicator_registry.register_indicator(self.first_tile)
        self.second_tile: Tile = Tile(
            rule_property=rule_properties.second_property,
            rule_id=self.rule_id
        )
        if self.second_tile.type == RulePropertyType.INDICATOR:
            self.indicator_registry.register_indicator(self.second_tile)
        self.comparison_method = RuleComparisonMethod(rule_properties.comparison.value)
        self.signals = Signals(
            signal_indexes=deepcopy(signal_indexes),
            order_type=self.order_type
        )

    @property
    def is_valid_rule(self) -> bool:
        """
        Checks if the rule is valid based on the tiles.
        """
        return self.first_tile != self.second_tile

    def __repr__(self) -> str:
        """
        Returns a string representation of the Rule.
        """
        return f"Rule(order_type={self.order_type}, " \
               f"first_tile={self.first_tile}, " \
               f"second_tile={self.second_tile}, " \
               f"comparison_method={self.comparison_method})"
