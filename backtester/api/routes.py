from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from backtester.api.dependencies import init_backtester
from backtester.api.requests.backtesting_request import BacktestingRequest
from backtester.api.responses.error_responses import error_responses
from backtester.api.responses.metadata import Metadata
from backtester.api.responses.success_response import SuccessResponse, SuccessResponseModel
from backtester.domain.strategy.presenters import StrategyGroupedStats
from fastapi import status

trading_system_router = APIRouter()


@trading_system_router.post(
    "/create",
    response_model=SuccessResponseModel[StrategyGroupedStats],
    status_code=status.HTTP_200_OK,
    summary="Create and Backtest Trading System",
    responses=error_responses
)
def create_trading_system(
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
