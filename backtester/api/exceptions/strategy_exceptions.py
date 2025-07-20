from fastapi import HTTPException


class InvalidTradeResultType(HTTPException):
    def __init__(self, trade_result:str):
        super().__init__(
            status_code=404,
            detail={
                "error": f"Invalid trade result {trade_result} requested.",
                "message": 'Encountered unexpected error... Please contact us for more information!'
            }
        )
