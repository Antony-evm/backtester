"""
This module provides the format for ticker requests within trade system requests
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from domain.enums.ticker_interval import TickerInterval


class TickerRequest(BaseModel):
    """
    The request model for ticker data retrieval.
    """
    ticker: str = Field(
        ...,
        description="Ticker for which to retrieve data for",
        examples=["AAPL"]
    )
    start_date: Optional[datetime] = Field(
        ...,
        description="Start date in ISO Format, minimum 1985-01-01",
        examples=["2025-01-01"]
    )
    end_date: Optional[datetime] = Field(
        ...,
        description="End date in ISO Format, maximum previous day",
        examples=["2025-01-02"]
    )
    interval: TickerInterval = Field(
        "1d",
        description="Interval each ticker period represents",
        examples=["1d"]
    )
