"""
Trade entity for backtesting module.
"""
import hashlib
import os
from datetime import datetime
from typing import List, Optional

from .thresholds import Thresholds
from .trading_period import TradingPeriod
from backtester.api.requests.portfolio_management import TradeSize, TradeTargets
from backtester.domain.enums.order_type import OrderType
from backtester.domain.enums.trade_size_type import TradeSizeType
from backtester.domain.enums.trade_result import TradeResult
from backtester.domain.enums.trading_period_result import TradingPeriodResult


class Trade:
    """
    Represents a trade in the backtesting module.
    """

    def __init__(
            self,
            starting_portfolio_amount: float,
            trade_size: TradeSize,
            trade_targets: TradeTargets,
            order_type: OrderType
    ):
        """
        Initializes a Trade instance.
        :param starting_portfolio_amount: starting amount of the portfolio for the trade.
        :param trade_size: trade size settings, either dynamic or static.
        :param trade_targets: trade targets including take profit and stop loss values.
        :param order_type: type of order for the trade (buy or sell).
        """
        self.id = hashlib.sha256(os.urandom(32)).hexdigest()
        self.starting_portfolio_amount = starting_portfolio_amount
        self.trade_size_type = TradeSizeType(trade_size.type)
        self.trade_size_value = trade_size.value
        self.take_profit = trade_targets.take_profit
        self.stop_loss = trade_targets.stop_loss
        self.order_type = order_type
        self.trading_periods: List[TradingPeriod] = []
        self.trade_returns = 1

    @property
    def entry_amount(self) -> float:
        """
        Calculates the entry amount for the trade based on the trade size type.
        :return: entry amount as a float.
        """
        if self.trade_size_type == TradeSizeType.DYNAMIC:
            amount = self.trade_size_value * self.starting_portfolio_amount
        elif self.trade_size_type == TradeSizeType.STATIC:
            amount = self.trade_size_value
        else:
            amount = 0
        return amount

    @property
    def current_amount(self) -> float:
        """
        Calculates the current amount of the trade based on the entry amount and trade returns.
        :return: current amount as a float rounded to 4 decimal places.
        """
        if self.order_type == OrderType.BUY:
            amount = self.entry_amount * self.trade_returns
        elif self.order_type == OrderType.SELL:
            amount = self.entry_amount * (2 - self.trade_returns)
        else:
            amount = self.entry_amount
        return round(amount, 4)

    @property
    def current_portfolio_amount(self) -> float:
        """
        Calculates the current portfolio amount after the trade.
        :return: current portfolio amount as a float.
        """
        return self.starting_portfolio_amount - self.entry_amount + self.current_amount

    @property
    def current_trading_period(self) -> Optional[TradingPeriod]:
        """
        Gets the current trading period of the trade.
        :return: the last trading period if available, otherwise None.
        """
        return self.trading_periods[-1] if self.trading_periods else None

    @property
    def trade_result(self) -> TradeResult:
        """
        Determines the result of the trade based on the current amount and entry amount.
        :return: TradeResult enum indicating the result of the trade.
        """
        if self.current_amount > self.entry_amount:
            return TradeResult.WIN
        if self.current_amount < self.entry_amount:
            return TradeResult.LOSS
        return TradeResult.UNDETERMINED

    @property
    def thresholds(self) -> Thresholds:
        """
        Calculates the thresholds for the trade based on the order type and trade targets.
        :return: Thresholds object containing upper and lower thresholds.
        """
        lower_threshold = 1 + self.stop_loss \
            if self.order_type == OrderType.BUY else 1 - self.take_profit
        upper_threshold = 1 + self.take_profit \
            if self.order_type == OrderType.BUY else 1 - self.stop_loss
        return Thresholds(
            upper=upper_threshold,
            lower=lower_threshold
        )

    @property
    def starting_period(self) -> Optional[datetime]:
        """
        Gets the starting period of the trade.
        """
        return self.trading_periods[0].start_date if self.trading_periods else None

    @property
    def ending_period(self) -> datetime:
        """
        Gets the ending period of the trade,
        which is the start date of the last trading period.
        """
        return self.trading_periods[-1].start_date if self.trading_periods else None

    @property
    def exit_period_result(self) -> Optional[TradingPeriodResult]:
        """
        Gets the result of the last trading period.
        """
        return self.trading_periods[-1].result if self.trading_periods else None

    @property
    def starting_period_open(self) -> Optional[float]:
        """
        Gets the opening price of the first trading period.
        """
        return self.trading_periods[0].ticker_price_open if self.trading_periods else None

    @property
    def exit_period_close(self) -> Optional[float]:
        """
        Gets the closing price of the last trading period.
        """
        return self.trading_periods[-1].ticker_price_close if self.trading_periods else None

    @property
    def exit_period_high(self) -> Optional[float]:
        """
        Gets the highest price of the last trading period.
        """
        return self.trading_periods[-1].ticker_price_high if self.trading_periods else None

    @property
    def exit_period_low(self) -> Optional[float]:
        """
        Gets the lowest price of the last trading period.
        """
        return self.trading_periods[-1].ticker_price_low if self.trading_periods else None

    @property
    def percentage_returns(self) -> float:
        """
        Calculates the percentage returns of the trade.
        """
        return self.trade_returns - 1

    @property
    def absolute_returns(self) -> float:
        """
        Calculates the absolute returns of the trade.
        """
        return self.current_amount - self.entry_amount

    def set_trade_returns(self, returns) -> None:
        """
        Sets the trade returns for the trade.
        :param returns: the returns to set for the trade.
        """
        self.trade_returns = returns

    def add_trading_period(self, trading_period) -> None:
        """
        Adds a trading period to the trade.
        :param trading_period: the TradingPeriod object to add.
        :return: None
        """
        self.trading_periods.append(trading_period)

    def __repr__(self) -> str:
        """
        Returns a string representation of the Trade instance.
        """
        return (
            f"Trade(id={self.id}, "
            f"starting_portfolio_amount={self.starting_portfolio_amount}, "
            f"trade_size={self.trade_size_type, self.trade_size_value}, "
            f"take_profit={self.take_profit}, "
            f"stop_loss={self.stop_loss}, "
            f"order_type={self.order_type}, "
            f"trading_periods_count={len(self.trading_periods)})"
        )
