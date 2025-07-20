import pandas as pd

from backtester.api.requests.backtesting_request import BacktestingRequest
from backtester.application.ticker_service import TickerService


class Backtester:
    def __init__(self, ticker_service: TickerService):
        self.ticker_service = ticker_service

    def backtest(
            self,
            backtesting_request: BacktestingRequest
    ) -> pd.DataFrame:
        df = self.ticker_service.fetch_ticker_data(backtesting_request.ticker_request)
        return df
