"""
TickerService for fetching ticker data.
"""
from api.requests.ticker_request import TickerRequest
from infrastructure.ticker_provider import TickerProvider
import pandas as pd


class TickerService:
    """
    Service for fetching ticker data using a TickerProvider.
    """

    def __init__(self, ticker_provider: TickerProvider):
        self.ticker_provider = ticker_provider

    def fetch_ticker_data(self, ticker_request: TickerRequest) -> pd.DataFrame:
        """
        Fetches ticker data based on the provided TickerRequest.
        :param ticker_request: request containing ticker, start date, end date, and interval
        :return: dataframe with ticker data
        """
        df = self.ticker_provider.fetch(
            ticker=ticker_request.ticker,
            interval=ticker_request.interval.value,
            start=ticker_request.start_date,
            end=ticker_request.end_date
        )
        return df
