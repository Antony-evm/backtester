"""
StatsField Presenter
"""
from typing import Optional

from pydantic import BaseModel


class StatsField(BaseModel):
    """
    Represents a way to present a single statistic in the backtesting results.
    """
    display_name: str
    type: str
    value: Optional[float | str | int]

    def __repr__(self):
        """
        Returns a string representation of the StatsField instance.
        """
        return (
            f"StatsField("
            f"display_name={self.display_name}, "
            f"type={self.type}, "
            f"value={self.value})"
        )
