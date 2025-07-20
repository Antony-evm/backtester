"""
Indicator Registry Module
"""
from typing import Any, Dict

from .tile import Tile


class IndicatorRegistry:
    """
    Holds indicator tiles and their associated data.
    """

    def __init__(self):
        """
        Initializes the IndicatorRegistry
        with empty dictionaries for indicators and their data.
        """
        self.indicators: Dict[str, Tile] = {}
        self.indicator_data: Dict[str, Any] = {}

    def register_indicator(self, tile: Tile) -> None:
        """
        Registers an indicator tile in the registry.
        :param tile: Tile object representing the indicator to be registered.
        """
        self.indicators[tile.id] = tile
        self.indicator_data[tile.id] = {
            'name': tile.name,
            'parameters': tile.parameters.model_dump()
        }

    def __repr__(self) -> str:
        """
        Returns a string representation of the IndicatorRegistry.
        """
        return (f"IndicatorRegistry("
                f"indicators={self.indicators},"
                f"indicator_data={self.indicator_data})"
                )
