"""
BacktestingGroup Presenter
"""
from pydantic import BaseModel

from .stats_field import StatsField


class BacktestingGroup(BaseModel):
    """
    Represents a group of backtesting statistics.
    """
    trades: StatsField
    wins: StatsField
    losses: StatsField
    win_rate: StatsField

    def __repr__(self) -> str:
        """
        Returns a string representation of the BacktestingGroup instance.
        """
        return (
            f"BacktestingGroup("
            f"trades={self.trades}, "
            f"wins={self.wins}, "
            f"losses={self.losses}, "
            f"win_rate={self.win_rate})"
        )
