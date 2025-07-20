from typing import List

from fastapi import HTTPException


class IndicatorNotFoundError(HTTPException):
    def __init__(self, indicator: str):
        super().__init__(
            status_code=404,
            detail={
                "error": f"Indicator {indicator} has not been implemented.",
                "message": 'Encountered unexpected error... Please contact us for more information!'
            }
        )


class IndicatorComputationError(HTTPException):
    def __init__(self, indicator: str):
        super().__init__(
            status_code=500,
            detail={
                "error": f"Encountered unexpected error while calculating {indicator}"
                         f" Check the logs for more information.",
                "message": 'Encountered unexpected error... Please contact us for more information!'
            }
        )


class MissingIndicatorParametersError(HTTPException):
    def __init__(self, indicator: str, missing_parameters: List[str]):
        super().__init__(
            status_code=500,
            detail={
                "error": f"Critical parameters are missing to calculate indicator {indicator}."
                         f" Missing parameters: {missing_parameters}",
                "message": 'Encountered unexpected error... Please contact us for more information!'
            }
        )
