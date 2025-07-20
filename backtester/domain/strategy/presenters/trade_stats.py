"""
TradeStats Presenter
"""
from pydantic import BaseModel

from backtester.domain.strategy.trade import Trade

from .stats_field import StatsField


class TradeStats(BaseModel):
    """
    Represents the statistics of a single trade after backtesting.
    """
    order_type: StatsField
    starting_portfolio_amount: StatsField
    current_portfolio_amount: StatsField
    entry_amount: StatsField
    current_amount: StatsField
    percentage_returns: StatsField
    absolute_returns: StatsField
    trade_result: StatsField
    starting_period: StatsField
    ending_period: StatsField
    trading_periods: StatsField
    exit_period_result: StatsField
    starting_period_open: StatsField
    exit_period_close: StatsField
    exit_period_high: StatsField
    exit_period_low: StatsField

    @classmethod
    def from_trade(cls, trade: Trade) -> "TradeStats":
        """
        Creates a TradeStats instance from a Trade entity.
        :param trade: Trade entity containing the statistics to be converted.
        :return: TradeStats instance with statistics from the Trade entity.
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
            order_type=wrap(
                "Order Type", "String", trade.order_type.value
            ),
            starting_portfolio_amount=wrap(
                "Starting Portfolio Amount",
                "Currency",
                trade.starting_portfolio_amount
            ),
            current_portfolio_amount=wrap(
                "Current Portfolio Amount",
                "Currency",
                trade.current_portfolio_amount
            ),
            entry_amount=wrap(
                "Entry Amount", "Currency", trade.entry_amount
            ),
            current_amount=wrap(
                "Exit Amount", "Currency", trade.current_amount
            ),

            percentage_returns=wrap(
                "ROI %", "Percentage", trade.percentage_returns
            ),
            absolute_returns=wrap(
                "ROI", "Currency", trade.absolute_returns
            ),
            trade_result=wrap(
                "Result", "String", trade.trade_result.value
            ),
            starting_period=wrap(
                "Entered at", "Date", trade.starting_period
            ),
            ending_period=wrap(
                "Exited at", "Date", trade.ending_period
            ),
            trading_periods=wrap(
                "Trading Periods", "Integer", len(trade.trading_periods)
            ),
            exit_period_result=wrap(
                "Exit Reason", "String", trade.exit_period_result.value
            ),
            starting_period_open=wrap(
                "Entry Period Open", "Currency", trade.starting_period_open
            ),
            exit_period_close=wrap(
                "Exit Period Close", "Currency", trade.exit_period_close
            ),
            exit_period_high=wrap(
                "Exit Period High", "Currency", trade.exit_period_high
            ),
            exit_period_low=wrap(
                "Exit Period Low", "Currency", trade.exit_period_low
            ),
        )

    def __repr__(self) -> str:
        """
        Returns a string representation of the TradeStats instance.
        """
        return (
            f"TradeStats("
            f"order_type={self.order_type}, "
            f"starting_portfolio_amount={self.starting_portfolio_amount}, "
            f"current_portfolio_amount={self.current_portfolio_amount}, "
            f"entry_amount={self.entry_amount}, "
            f"current_amount={self.current_amount}, "
            f"percentage_returns={self.percentage_returns}, "
            f"absolute_returns={self.absolute_returns}, "
            f"trade_result={self.trade_result}, "
            f"starting_period={self.starting_period}, "
            f"ending_period={self.ending_period}, "
            f"trading_periods={self.trading_periods}, "
            f"exit_period_result={self.exit_period_result}, "
            f"starting_period_open={self.starting_period_open}, "
            f"exit_period_close={self.exit_period_close}, "
            f"exit_period_high={self.exit_period_high}, "
            f"exit_period_low={self.exit_period_low})"
        )
