"""
StrategyStats Presenter
"""
from typing import Dict

from pydantic import BaseModel


from .stats_field import StatsField
from .trade_stats import TradeStats
from backtester.domain.strategy.strategy import Strategy


class StrategyStats(BaseModel):
    """
    Represents the statistics of a trading strategy after backtesting.
    """
    trades: StatsField
    wins: StatsField
    losses: StatsField
    win_rate: StatsField
    percentage_returns: StatsField
    absolute_returns: StatsField
    starting_amount: StatsField
    current_amount: StatsField
    trade_stats: Dict[int, TradeStats]

    @classmethod
    def from_strategy(cls, strategy: Strategy) -> "StrategyStats":
        """
        Creates a StrategyStats instance from a Strategy entity.
        :param strategy: Strategy entity containing the statistics to be converted.
        :return: StrategyStats instance with statistics from the Strategy entity.
        """

        def wrap(name: str, typ: str, val) -> StatsField:
            """
            Wraps a statistic in a StatsField for presentation.
            :param name: name of the statistic to be displayed.
            :param typ: type of the statistic (e.g., "Integer", "Percentage", "Currency").
            :param val: value of the statistic to be wrapped.
            :return: StatsField instance containing the statistic.
            """
            return StatsField(display_name=name, type=typ, value=val)

        return cls(
            trades=wrap("Trades", "Integer", strategy.trades),
            wins=wrap("Wins", "Integer", strategy.wins),
            losses=wrap("Losses", "Integer", strategy.losses),
            win_rate=wrap("Win Rate", "Percentage", strategy.win_rate),

            percentage_returns=wrap(
                "ROI %", "Percentage", strategy.percentage_returns
            ),
            absolute_returns=wrap(
                "ROI", "Currency", strategy.absolute_returns
            ),
            starting_amount=wrap(
                "Starting Amount", "Currency", strategy.starting_amount
            ),
            current_amount=wrap(
                "Current Amount", "Currency", strategy.current_amount
            ),
            trade_stats={
                i: TradeStats.from_trade(trade)
                for i, trade in enumerate(strategy.all_trades)
            },
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the StrategyStats instance.
        """
        return (
            f"StrategyStats("
            f"trades={self.trades}, "
            f"wins={self.wins}, "
            f"losses={self.losses}, "
            f"win_rate={self.win_rate}, "
            f"percentage_returns={self.percentage_returns}, "
            f"absolute_returns={self.absolute_returns}, "
            f"starting_amount={self.starting_amount}, "
            f"current_amount={self.current_amount}, "
            f"trade_stats={self.trade_stats})"
        )
