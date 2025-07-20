"""
StrategyGroupedStats Presenter
"""
from typing import Dict

from pydantic import BaseModel

from .backtesting_group import BacktestingGroup
from .profitability_group import ProfitabilityGroup
from .strategy_stats import StrategyStats
from .trade_stats import TradeStats


class StrategyGroupedStats(BaseModel):
    """
    Represents a grouped view of strategy statistics for backtesting.
    """
    Backtesting: BacktestingGroup
    Profitability: ProfitabilityGroup
    Trades: Dict[int, TradeStats]

    @classmethod
    def from_strategy_stats(cls, stats: "StrategyStats") -> "StrategyGroupedStats":
        """
        Creates a StrategyGroupedStats instance from a StrategyStats instance.
        :param stats: StrategyStats instance containing the statistics to be grouped.
        :return: StrategyGroupedStats instance with grouped statistics.
        """
        return cls(
            Backtesting=BacktestingGroup(
                trades=stats.trades,
                wins=stats.wins,
                losses=stats.losses,
                win_rate=stats.win_rate
            ),
            Profitability=ProfitabilityGroup(
                percentage_returns=stats.percentage_returns,
                absolute_returns=stats.absolute_returns,
                starting_amount=stats.starting_amount,
                current_amount=stats.current_amount
            ),
            Trades=stats.trade_stats,
            ticker_data={}
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the StrategyGroupedStats instance.
        """
        return (
            f"StrategyGroupedStats("
            f"Backtesting={self.Backtesting}, "
            f"Profitability={self.Profitability}, "
            f"Trades={self.Trades}, "
        )
