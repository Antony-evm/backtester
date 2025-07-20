import logging
from typing import Set

import pandas as pd

from backtester.api.requests.backtesting_request import BacktestingRequest
from backtester.api.requests.portfolio_management import PortfolioManagement
from backtester.application.signal_service import SignalService
from backtester.application.strategy_service import StrategyService
from backtester.application.ticker_service import TickerService
from backtester.application.trade_service import TradeService
from backtester.domain.enums.order_type import OrderType
from backtester.domain.strategy.presenters import StrategyGroupedStats, StrategyStats

logger = logging.getLogger(__name__)


class Backtester:
    def __init__(
            self,
            ticker_service: TickerService,
            signal_service: SignalService,
            strategy_service: StrategyService,
            trade_service: TradeService
    ):
        self.ticker_service = ticker_service
        self.signal_service = signal_service
        self.strategy_service = strategy_service
        self.trade_service = trade_service

    def backtest(
            self,
            backtesting_request: BacktestingRequest
    ) -> StrategyGroupedStats:
        ticker_data = self.ticker_service.fetch_ticker_data(backtesting_request.ticker_request)

        trading_system_rules = self.signal_service.process_trading_system_rules(
            ticker_data=ticker_data,
            trading_system_rules=backtesting_request.trading_system_rules,
        )
        self.signal_service.calculate_indicators(
            ticker_data=ticker_data,
        )

        ticker_data = self.signal_service.calculate_rules_mask(
            ticker_data=ticker_data.copy(),
            trading_system_rule=trading_system_rules
        )
        self.signal_service.process_trading_system_rules(
            ticker_data=ticker_data,
            trading_system_rules=backtesting_request.trading_system_rules,
        )
        return self._run_backtest(
            ticker_data=ticker_data,
            portfolio_management=backtesting_request.portfolio_management,
        )

    def _run_backtest(
            self,
            ticker_data: pd.DataFrame,
            portfolio_management: PortfolioManagement,
    ) -> StrategyGroupedStats:
        """
        Runs a backtest on the provided ticker data
         using the specified portfolio management settings.
        :param ticker_data: The DataFrame containing ticker data with signals.
        :param portfolio_management: portfolio management settings for the backtest.
        :return: The results of the backtest, grouped by strategy.
        """
        signals = ticker_data[ticker_data['signal'] != OrderType.NO_ACTION].index
        processed_signals: Set[int] = set()

        strategy = self.strategy_service.init_strategy(
            portfolio_management=portfolio_management,
        )
        logger.debug("Starting backtest for strategy %s", strategy)
        for signal in signals:
            if signal in processed_signals:
                continue
            processed_signals.add(signal)
            order_type = ticker_data.at[signal, 'signal']
            trade = self.trade_service.init_trade(strategy=strategy, order_type=order_type)

            for i, (index, row) in enumerate(ticker_data.iloc[signal + 1:].iterrows()):
                self.trade_service.process_trading_period(
                    trade=trade,
                    trading_period_data=row,
                    is_first_trading_period=(i == 0)
                )
                logger.debug(
                    'Processing trading period %s',
                    trade.trading_periods[-1]
                )
                if trade.current_trading_period.result.end_trade:
                    logger.debug("Trade %s ended", trade)
                    break
                if index in signals:
                    processed_signals.add(index)

            self.strategy_service.process_trade_results(trade, strategy)
            logger.debug(
                "Processed trade %s successfully",
                trade.id
            )

        results = StrategyStats.from_strategy(strategy)
        return StrategyGroupedStats.from_strategy_stats(results)
