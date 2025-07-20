from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backtester.api.dependencies import init_backtester
from backtester.api.requests.backtesting_request import BacktestingRequest
from backtester.api.responses.metadata import Metadata
from backtester.api.responses.success_response import SuccessResponse

trading_system_router = APIRouter()


@trading_system_router.post(
    "/create",
)
async def create_trading_system(
        backtesting_request: BacktestingRequest,
        backtester=Depends(init_backtester),
):
    """
    Create a trading system and evaluate its performance.
    """
    start_time = datetime.now(timezone.utc)
    results = backtester.backtest(
        backtesting_request=backtesting_request
    )
    return SuccessResponse(
        response_data=results,
        metadata=Metadata.from_start_time(start_time)
    )
