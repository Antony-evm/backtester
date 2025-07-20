from datetime import datetime, timedelta, date
from typing import Optional, Union
import logging

from pydantic import BaseModel, root_validator

from backtester.api.exceptions.ticker_request_exceptions import MalformedTickerDatesError, TickerMinEndDateError, \
    TickerMaxStartDateError
from backtester.domain.enums.ticker_interval import TickerInterval

logger = logging.getLogger(__name__)

MIN_START_DATE = datetime(1985, 1, 1)
MAX_END_DATE = datetime.combine(datetime.now() - timedelta(days=1), datetime.min.time())


class TickerRequest(BaseModel):
    """
    Request model for ticker data retrieval.
    Includes validation and normalization of start/end dates.
    """
    ticker: str
    start_date: Optional[Union[date, datetime]] = None
    end_date: Optional[Union[date, datetime]] = None
    interval: TickerInterval = TickerInterval.DAILY

    @staticmethod
    def _parse_date(value) -> Optional[datetime]:
        if isinstance(value, str) and value.strip():
            return datetime.strptime(value, "%Y-%m-%d")
        logger.debug("Unable to parse date from value: %s", value)
        return None

    @staticmethod
    def _normalize_start_date(start: Optional[Union[date, datetime]]) -> Optional[Union[date, datetime]]:
        if not start:
            return MIN_START_DATE
        if start < MIN_START_DATE:
            logger.warning("Start date %s is before allowed minimum. Truncating.", start)
            return MIN_START_DATE
        if start > MAX_END_DATE:
            logger.error("Start date %s is after today.", start)
            raise TickerMaxStartDateError(start)
        return start

    @staticmethod
    def _normalize_end_date(end: Optional[Union[date, datetime]]) -> Optional[Union[date, datetime]]:
        if not end or end > MAX_END_DATE:
            logger.warning("End date is missing or in future. Truncating to yesterday.")
            return MAX_END_DATE
        if end.timestamp() < MIN_START_DATE.timestamp():
            logger.error("End date %s is before start date.", end)
            raise TickerMinEndDateError(end)
        return end

    @root_validator(pre=True)
    def convert_dates(cls, values):
        start = cls._parse_date(values.get("start_date"))
        end = cls._parse_date(values.get("end_date"))

        values["start_date"] = cls._normalize_start_date(start)
        values["end_date"] = cls._normalize_end_date(end)
        return values

    @root_validator
    def validate_date_order(cls, values):
        """
        POST-validation: ensure end_date > start_date.
        """
        start_ts = values.get("start_date")
        end_ts = values.get("end_date")
        if start_ts is not None and end_ts <= start_ts:
            logger.error(
                "End date must be after start date. Got start: %s, end: %s",
                start_ts, end_ts
            )
            raise MalformedTickerDatesError(start_ts, end_ts)
        return values

    def __repr__(self) -> str:
        return (
            f"<TickerRequest(ticker={self.ticker}, "
            f"start_date={self.start_date}, end_date={self.end_date}, interval={self.interval})>"
        )
