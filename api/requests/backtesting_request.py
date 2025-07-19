"""
Trading System Request Model
"""
from pydantic import BaseModel, Field

from .portfolio_management import PortfolioManagement
from .ticker_request import TickerRequest
from .trading_system import TradingSystem


class BacktestingRequest(BaseModel):
    """
    Request model for trading system configurations.
    """
    ticker_request: TickerRequest
    # portfolio_management: PortfolioManagement
    # trading_system: TradingSystem
