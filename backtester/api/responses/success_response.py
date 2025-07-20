from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from typing import Optional, Any, TypeVar, Generic
from .metadata import Metadata


class SuccessResponse(JSONResponse):
    def __init__(
            self,
            metadata: Metadata,
            response_data: Optional[Any] = None,
    ):
        super().__init__(
            status_code=status.HTTP_200_OK,
            content={
                "data": (
                            response_data.dict()
                            if isinstance(response_data, BaseModel)
                            else response_data
                        ) or {},
                "metadata": metadata.dict()
            }
        )


DataT = TypeVar("DataT")


class SuccessResponseModel(BaseModel, Generic[DataT]):
    data: Optional[DataT] = None
    metadata: Metadata
