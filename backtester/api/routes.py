from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from backtester.api.dependencies import init_backtester
from backtester.api.requests.backtesting_request import BacktestingRequest

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
    return JSONResponse(
        content={
            "message": "Trading system created successfully",
            "results": results.to_dict(),
            "execution_time": (datetime.now(timezone.utc) - start_time).total_seconds()
        }
    )
