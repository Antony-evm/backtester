from fastapi import HTTPException


class TickerDataNotFound(HTTPException):
    """
    Exception for when the provider does not return data for the ticker
    """

    def __init__(self, ticker: str):
        super().__init__(
            status_code=404,
            detail={
                "error": f"Provider did not return data for {ticker}.",
                "message": "Encountered unexpected error... Please contact us for more information!"
            }
        )
