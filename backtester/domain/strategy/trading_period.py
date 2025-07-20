"""
Trading Period Entity
"""
import pandas as pd

from backtester.domain.enums.order_type import OrderType
from backtester.domain.enums.trading_period_result import TradingPeriodResult
from backtester.domain.strategy.thresholds import Thresholds


class TradingPeriod:
    """
    Represents a trading period in the backtesting module.
    """

    def __init__(
            self,
            trade_returns: float,
            order_type: OrderType,
            thresholds: Thresholds,
            trading_period_data: pd.Series,
            is_first_trading_period: bool
    ):
        """
        Initializes a TradingPeriod instance.
        :param trade_returns: current returns from the trade.
        :param order_type: type of order for the trade (buy or sell).
        :param thresholds: thresholds for the trading period, including upper and lower limits.
        :param trading_period_data: data for the trading period,
         including date, signal, and price information.
        :param is_first_trading_period: indicates if this is the first trading period
        """
        self.trade_returns = trade_returns
        self.trading_period_data = trading_period_data
        self.upper_threshold = thresholds.upper
        self.lower_threshold = thresholds.lower
        self.order_type = order_type
        self.is_first_trading_period = is_first_trading_period
        self.start_date = trading_period_data['date']
        self.trading_period_signal: OrderType = trading_period_data['signal']
        self.ticker_price_open = trading_period_data['open']
        self.ticker_price_close = trading_period_data['close']
        self.ticker_price_high = trading_period_data['high']
        self.ticker_price_low = trading_period_data['low']
        self.returns_on_low = 1 + trading_period_data[
            "returns_on_low_same_day" if is_first_trading_period else "returns_on_low"
        ]
        self.returns_on_high = 1 + trading_period_data[
            "returns_on_high_same_day" if is_first_trading_period else "returns_on_high"
        ]
        self.returns_on_close = 1 + trading_period_data[
            "returns_on_close_same_day" if is_first_trading_period else "returns_on_close"
        ]

    @property
    def result(self) -> TradingPeriodResult:
        """
        Determines the result of the trading period based on the thresholds and signals.
        """
        if self._is_upper_limit_hit():
            return TradingPeriodResult.HIGHER_LIMIT
        if self._is_lower_limit_hit():
            return TradingPeriodResult.LOWER_LIMIT
        if self._is_opposite_signal_encountered():
            return TradingPeriodResult.OPPOSING_TRADE
        return TradingPeriodResult.CONTINUE_TRADE

    def _is_opposite_signal_encountered(self) -> bool:
        """
        Checks if the trading period signal is opposite to the order type.
        """
        return self.order_type.opposite == self.trading_period_signal

    def _is_lower_limit_hit(self) -> bool:
        """
        Checks if the lower limit of the trade has been hit.
        """
        return self.trade_returns * self.returns_on_low <= self.lower_threshold

    def _is_upper_limit_hit(self) -> bool:
        """
        Checks if the upper limit of the trade has been hit.
        """
        return self.trade_returns * self.returns_on_high >= self.upper_threshold

    @property
    def trading_period_returns(self) -> float:
        """
        Calculates the returns for the trading period based on the result.
        """
        if self.result == TradingPeriodResult.HIGHER_LIMIT:
            return self.upper_threshold
        if self.result == TradingPeriodResult.LOWER_LIMIT:
            return self.lower_threshold

        return self.trade_returns * self.returns_on_close

    def __repr__(self) -> str:
        """
        Returns a string representation of the TradingPeriod instance
        """
        return f"TradingPeriod(start_date={self.start_date}, " \
               f"trade_returns={self.trade_returns}, " \
               f"order_type={self.order_type}, " \
               f"result={self.result})"
