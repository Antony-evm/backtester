"""
Tile Entity
"""
import hashlib
import os
from typing import List

import pandas as pd

from backtester.api.requests.trading_system import RuleProperty
from backtester.domain.enums.rule_property_type import RulePropertyType


class Tile:
    """
    Represents a tile within a strategy block.
    """

    def __init__(
            self,
            rule_property: RuleProperty,
            rule_id: str
    ):
        """
        Initializes a Tile instance.
        :param rule_property: RuleProperty, containing the properties of the rule
        :param rule_id: ID of the rule
        """
        self.rule_id = rule_id
        self.id = hashlib.sha256(os.urandom(32)).hexdigest()
        self.type = RulePropertyType(rule_property.type)
        self.name = rule_property.name
        self.parameters = rule_property.parameters
        self.mask: pd.Series = pd.Series()

    def __eq__(self, other) -> bool:
        """
        Compares two Tile instances for equality.
        :param other: Another Tile instance to compare against.
        :return: True if both instances are equal, False otherwise.
        """
        return (
                self.type == other.type and
                self.name == other.name and
                self.parameters == other.parameters
        )

    def set_mask(self, mask: List) -> None:
        """
        Sets the mask for the tile.
        :param mask: List of boolean values representing the mask.
        """
        self.mask = pd.Series(mask)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Tile instance.
        """
        return f"Tile(id={self.id}, type={self.type}, name={self.name}, " \
               f"parameters={self.parameters}, " \
               f"rule_id={self.rule_id})"
