"""
TickerService for fetching ticker data.
"""
from backtester.api.requests.ticker_request import TickerRequest
from backtester.application.ticker_data_processor import TickerDataProcessor
from backtester.infrastructure.ticker_provider import TickerProvider
import pandas as pd
import logging

logger = logging.getLogger(__name__)


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
        df = self._process_ticker_data(df)
        return df

    @staticmethod
    def _process_ticker_data(
            df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Apply transformations to prepare ticker data for downstream use.
        :param df: Raw DataFrame containing ticker data.
        :return: df with helper columns added and date converted to ISO format.
        """
        df = TickerDataProcessor.add_helper_columns(df)
        logger.debug(
            "Helper columns added to ticker data: %s", df.columns
        )
        df = TickerDataProcessor.convert_date_to_isoformat(df)
        return df
