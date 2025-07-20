"""
ProfitabilityGroup Presenter
"""
from pydantic import BaseModel

from .stats_field import StatsField


class ProfitabilityGroup(BaseModel):
    """
    Represents a group of profitability statistics for backtesting.
    """
    percentage_returns: StatsField
    absolute_returns: StatsField
    starting_amount: StatsField
    current_amount: StatsField

    def __repr__(self) -> str:
        """
        Returns a string representation of the ProfitabilityGroup instance.
        """
        return (
            f"ProfitabilityGroup("
            f"percentage_returns={self.percentage_returns}, "
            f"absolute_returns={self.absolute_returns}, "
            f"starting_amount={self.starting_amount}, "
            f"current_amount={self.current_amount})"
        )
