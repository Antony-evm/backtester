import pandas as pd

from backtester.api.requests.backtesting_request import BacktestingRequest
from backtester.application.signal_service import SignalService
from backtester.application.ticker_service import TickerService


class Backtester:
    def __init__(
            self,
            ticker_service: TickerService,
            signal_service: SignalService
    ):
        self.ticker_service = ticker_service
        self.signal_service = signal_service

    def backtest(
            self,
            backtesting_request: BacktestingRequest
    ) -> pd.DataFrame:
        df = self.ticker_service.fetch_ticker_data(backtesting_request.ticker_request)
        trading_system_rules = self.signal_service.process_trading_system_rules(
            ticker_data=df,
            trading_system_rules=backtesting_request.trading_system_rules,
            trading_system_id=backtesting_request.trading_system_id,
        )
        return df
