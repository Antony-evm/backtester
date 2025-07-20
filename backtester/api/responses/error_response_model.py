from pydantic import BaseModel


class ErrorResponseModel(BaseModel):
    error: str
    message: str
