"""
Exceptions related to invalid ticker requests.
"""

from datetime import datetime
from fastapi import HTTPException, status


class InvalidTickerDateRequest(HTTPException):
    """
    Base class for ticker date validation errors.
    """

    def __init__(self, error: str, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "error": error,
                "message": message
            }
        )


class MalformedTickerDatesError(InvalidTickerDateRequest):
    """
    Raised when the start date is after the end date.
    """

    def __init__(self, start_date: datetime, end_date: datetime):
        super().__init__(
            error=(
                f"Start date must be before end date. "
                f"Received start date {start_date} and end date {end_date}."
            ),
            message=(
                f"Start date must be before end date. "
                f"Received start date {start_date} and end date {end_date}. "
                "Please increase the date range requested."
            )
        )


class TickerMinEndDateError(InvalidTickerDateRequest):
    """
    Raised when the end date is before 1985-01-01.
    """

    def __init__(self, end_date: datetime):
        super().__init__(
            error=(
                f"End date cannot be earlier than 1985-01-01. "
                f"Received end date {end_date}."
            ),
            message=(
                f"End date cannot be earlier than 1985-01-01. "
                f"Received end date {end_date}."
            )
        )


class TickerMaxStartDateError(InvalidTickerDateRequest):
    """
    Raised when the start date is after today's date.
    """

    def __init__(self, start_date: datetime):
        super().__init__(
            error=(
                f"Start date cannot be after today's date. "
                f"Received start date {start_date}."
            ),
            message=(
                f"Start date cannot be after today's date. "
                f"Received start date {start_date}."
            )
        )
