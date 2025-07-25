"""
Trading System Rules Module
"""
from typing import Dict, Optional

from pydantic import BaseModel

from backtester.domain.enums.order_type import OrderType
from backtester.domain.enums.rule_comparison_method import RuleComparisonMethod


class TilePropertyParameters(BaseModel):
    """
    Represents parameters for a tile property,
    """
    timeperiod: Optional[int] = None
    value: Optional[int] = None


class RuleProperty(BaseModel):
    """
    Represents a property of a rule
     that can be compared with another property.
    """
    type: str
    name: Optional[str] = None
    parameters: TilePropertyParameters


class Comparison(BaseModel):
    """
    Represents a comparison operation between two rule properties.
    """
    value: RuleComparisonMethod


class RuleProperties(BaseModel):
    """
    Represents properties of a rule that compares two rule properties.
    """
    first_property: RuleProperty
    comparison: Comparison
    second_property: RuleProperty
    rule_id: str


class GroupRules(BaseModel):
    """
    Represents a group of rules for a specific order type.
    """
    rules: Dict[str, RuleProperties]
    group_rule_id: str


class OrderTypeRules(BaseModel):
    """
    Represents the rules for a specific order type
    """
    group_rules: Dict[str, GroupRules]
    order_type_rule_id: Optional[str] = None


class TradingSystemRules(BaseModel):
    """
    Represents the trading system rules for different order types.
    """
    __root__: Dict[OrderType, OrderTypeRules]

