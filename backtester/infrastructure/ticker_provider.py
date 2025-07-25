from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, Union

import yfinance as yf
import pandas as pd

from backtester.api.exceptions.ticker_provider_exceptions import TickerDataNotFound

logger = logging.getLogger(__name__)


class TickerProvider:
    """
    Simple facade around yfinance.download that converts a `TickerRequest`
    into a pandas DataFrame.
    """

    def __init__(self):
        pass

    @staticmethod
    def fetch(
            ticker: str,
            interval: str,
            start: Optional[Union[str, datetime]],
            end: Optional[Union[str, datetime]]
    ) -> pd.DataFrame:
        """
        - ticker : str
            One ticker symbol, e.g. "AAPL"
        - interval : Optional[str], default = "1d"
            Valid values: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d,
                      5d, 1wk, 1mo, 3mo.
        - start : Optional[Union[str, datetime]]
            Inclusive start date (YYYY‑MM‑DD or datetime).
        - end : Optional[Union[str, datetime]]
        Exclusive end date (YYYY‑MM‑DD or datetime).  Defaults to *now*.
       :return:
       """

        df = yf.download(
            tickers=ticker,
            interval=interval,
            start=start,
            end=end,
            multi_level_index=False,
        ).reset_index().drop(columns=['Volume']).rename(
            columns={
                'Date': 'date',
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
            }
        )
        if df.empty:
            logger.error("No data found for ticker: %s", ticker)
            raise TickerDataNotFound(ticker=ticker)

        return df
