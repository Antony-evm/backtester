"""
This module provides the StrategyService class
"""
import logging

from backtester.api.exceptions.strategy_exceptions import InvalidTradeResultType
from backtester.api.requests.portfolio_management import PortfolioManagement
from backtester.domain.enums.trade_result import TradeResult
from backtester.domain.strategy.strategy import Strategy
from backtester.domain.strategy.trade import Trade

logger = logging.getLogger(__name__)


class StrategyService:
    """
    StrategyService class for managing strategies in backtesting.
    """

    def __init__(
            self
    ):
        pass

    @staticmethod
    def init_strategy(
            portfolio_management: PortfolioManagement,
    ) -> Strategy:
        """
        Initializes a Strategy instance.
        :param portfolio_management: Portfolio object containing trade size and targets
        :return: Strategy instance
        """
        return Strategy(
            portfolio_management=portfolio_management,
        )

    async def process_trade_results(
            self,
            trade: Trade,
            strategy: Strategy
    ) -> None:
        """
        Processes the results of a trade and updates the strategy accordingly.
        :param trade: Trade object containing trade details and results
        :param strategy: Strategy object to update with trade results
        """
        logger.debug(
            "Processing trade results for trade ID: %s",
            trade.id,
        )
        if not self._is_actionable_trade(trade):
            return
        self._process_trade_results(
            strategy=strategy,
            trade=trade
        )
        logger.debug(
            "Trade %s processed with result %s",
            trade,
            trade.trade_result,
        )
        strategy.set_current_amount(trade.current_portfolio_amount)
        strategy.add_trade_object(trade)

    @staticmethod
    def _is_actionable_trade(
            trade: Trade
    ) -> bool:
        """
        Checks if the trade is actionable based on its trade result.
        :param trade: Trade object to check
        :return: True if the trade is actionable, False otherwise
        """
        return trade.trade_result.actionable

    @staticmethod
    def _process_trade_results(
            strategy: Strategy,
            trade: Trade
    ) -> None:
        """
        Processes the trade results and updates the strategy's win/loss counts.
        :param strategy: Strategy object to update
        :param trade: Trade object containing trade results
        """
        if trade.trade_result == TradeResult.WIN:
            logger.debug(
                'Trade %s resulted in a win',
                trade.id,
            )
            strategy.add_win()
        elif trade.trade_result == TradeResult.LOSS:
            logger.debug(
                'Trade %s resulted in a loss',
                trade.id,
            )
            strategy.add_loss()
        else:
            logger.error(
                'Received invalid result %s for trade %s during processing request %s',
                trade.trade_result,
                trade.id
            )
            raise InvalidTradeResultType(
                trade_result=trade.trade_result.value
            )
        strategy.add_trade()
