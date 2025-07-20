"""
Rule class represents a trading rule in a strategy.
"""
from copy import deepcopy

import pandas as pd

from modules.strategy_service.api.requests.trading_system_rules import \
    RuleProperties
from modules.strategy_service.enums_shared.order_type import OrderType
from modules.strategy_service.interfaces.signal.domain.enums import (
    RuleComparisonMethod, RulePropertyType)

from .indicator_registry import IndicatorRegistry
from .signals import Signals
from .tile import Tile


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
            customer_id: str,
            group_rule_id: str,
            indicator_registry: IndicatorRegistry
    ):
        """
        Initializes a Rule instance.
        """
        self.customer_id = customer_id
        self.group_rule_id = group_rule_id
        self.rule_id = rule_properties.rule_id
        self.signal_indexes = signal_indexes
        self.order_type = order_type
        self.indicator_registry = indicator_registry
        self.first_tile: Tile = Tile(
            rule_property=rule_properties.first_property,
            customer_id=self.customer_id,
            rule_id=self.rule_id
        )
        if self.first_tile.type == RulePropertyType.INDICATOR:
            self.indicator_registry.register_indicator(self.first_tile)
        self.second_tile: Tile = Tile(
            rule_property=rule_properties.second_property,
            customer_id=self.customer_id,
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
