from fastapi import status

from backtester.api.responses.error_response_model import ErrorResponseModel

error_responses = {
    status.HTTP_404_NOT_FOUND: {
        "model": ErrorResponseModel,
        "description": "Resource not found",
        "content": {
            "application/json": {
                "examples": {
                    "TickerNotFound": {
                        "summary": "Ticker data not found",
                        "value": {
                            "error": "Provider did not return data for MSFT.",
                            "message": "Encountered unexpected error... Please contact us for more information!"
                        }
                    },
                    "IndicatorNotFound": {
                        "summary": "Indicator not supported",
                        "value": {
                            "error": "Indicator MACD has not been implemented.",
                            "message": "Encountered unexpected error... Please contact us for more information!"
                        }
                    }
                }
            }
        }
    },
    status.HTTP_422_UNPROCESSABLE_ENTITY: {
        "model": ErrorResponseModel,
        "description": "Validation error in request input",
        "content": {
            "application/json": {
                "example": {
                    "error": "Start date must be before end date. Received start date 2024-01-01 and end date "
                             "2020-01-01.",
                    "message": "Start date must be before end date. Received start date 2024-01-01 and end date "
                               "2020-01-01. Please increase the date range requested."
                }
            }
        }
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorResponseModel,
        "description": "Server-side processing error",
        "content": {
            "application/json": {
                "examples": {
                    "MissingIndicatorParameters": {
                        "summary": "Required parameters are missing",
                        "value": {
                            "error": "Critical parameters are missing to calculate indicator RSI. Missing parameters: "
                                     "['period']",
                            "message": "Encountered unexpected error... Please contact us for more information!"
                        }
                    },
                    "IndicatorComputationError": {
                        "summary": "Unexpected error while computing indicator",
                        "value": {
                            "error": "Encountered unexpected error while calculating RSI. Check the logs for more "
                                     "information.",
                            "message": "Encountered unexpected error... Please contact us for more information!"
                        }
                    }
                }
            }
        }
    }
}
