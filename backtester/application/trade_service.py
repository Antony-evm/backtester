"""
Trade Service for managing trades in a backtesting environment.
"""
import logging

import pandas as pd

from backtester.domain.enums.order_type import OrderType
from backtester.domain.strategy.strategy import Strategy
from backtester.domain.strategy.trade import Trade
from backtester.domain.strategy.trading_period import TradingPeriod

logger = logging.getLogger(__name__)


class TradeService:
    """
    TradeService class for managing trades in backtesting.
    """

    def __init__(self):
        """
        Initializes the TradeService.
        """

    @staticmethod
    def init_trade(
            strategy: Strategy,
            order_type: OrderType
    ) -> Trade:
        """
        Initializes a Trade instance based on the provided strategy and order type.
        :param strategy: Strategy instance containing trade details
        :param order_type: OrderType indicating the type of trade (e.g., BUY, SELL)
        :return: Trade instance initialized with strategy details and order type
        """
        return Trade(
            starting_portfolio_amount=strategy.current_amount,
            trade_size=strategy.trade_size,
            trade_targets=strategy.trade_targets,
            order_type=order_type
        )

    @staticmethod
    def _init_trading_period(
            trade: Trade,
            trading_period_data: pd.Series,
            is_first_trading_period: bool
    ) -> TradingPeriod:
        """
        Initializes a TradingPeriod instance for the given trade and trading period data.
        :param trade: Trade instance containing trade details
        :param trading_period_data: pd.Series containing trading period data
        :param is_first_trading_period: Boolean indicating if this is the first trading period
        :return: TradingPeriod instance initialized with trade details and trading period data
        """
        trading_period = TradingPeriod(
            trade_returns=trade.trade_returns,
            order_type=trade.order_type,
            thresholds=trade.thresholds,
            trading_period_data=trading_period_data,
            is_first_trading_period=is_first_trading_period
        )
        return trading_period

    def process_trading_period(
            self,
            trade: Trade,
            trading_period_data: pd.Series,
            is_first_trading_period: bool
    ) -> None:
        """
        Processes a trading period for the given trade
         and updates the trade with the new trading period.
        :param trade: Trade instance to process
        :param trading_period_data: pd.Series containing trading period data
        :param is_first_trading_period: Boolean indicating if this is the first trading period
        """
        logger.debug(
            "Processing trading period for trade %s with data %s",
            trade,
            trading_period_data
        )
        trading_period = self._init_trading_period(
            trade,
            trading_period_data,
            is_first_trading_period
        )
        trade.add_trading_period(trading_period)
        trade.set_trade_returns(
            trade.current_trading_period.trading_period_returns
        )
        logger.debug(
            "Trading period processed and added to trade %s",
            trade
        )
