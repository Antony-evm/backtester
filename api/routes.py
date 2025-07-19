from datetime import datetime, timezone

from backtesting_io_manager.response_models import (Metadata, SuccessResponse,
                                                    SuccessResponseModel)
from fastapi import APIRouter, Depends


trading_system_router = APIRouter()


@trading_system_router.post(
    "/backtest",
)
async def create_trading_system(
        trading_system_service=Depends(init_trading_system_service),
) -> SuccessResponse:
    """
    Create a trading system and evaluate its performance.
    """
    start_time = datetime.now(timezone.utc)

    return SuccessResponse(
        response_data=results,
        metadata=Metadata.from_start_time(start_time)
    )