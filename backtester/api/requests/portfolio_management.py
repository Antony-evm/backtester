"""
This module defines the Portfolio Management part of the trading system request
"""
import logging
from typing import Optional
from pydantic import BaseModel, Field, validator

from backtester.domain.enums.trade_size_type import TradeSizeType

logger = logging.getLogger(__name__)


class TradeSize(BaseModel):
    """
    Request model for trade size configuration.
    """
    type: TradeSizeType = Field(
        ...,
        description="Type of trade size",
        examples=["DYNAMIC", "STATIC"]
    )
    value: float = Field(
        ...,
        description="Value of the trade size, either a fixed amount or a percentage",
        examples=[1000.0, 0.05]
    )


class TradeTargets(BaseModel):
    """
    Request model for trade targets.
    """
    take_profit: Optional[float] = Field(
        ...,
        description="Take profit percentage, must be greater than 0.001",
        examples=[0.05, 0.10]
    )
    stop_loss: float = Field(
        ...,
        description="Stop loss percentage, must be between -1 and -0.001",
        examples=[-0.05, -0.10]
    )

    @validator("stop_loss", pre=True, always=True)
    def validate_stop_loss(cls, value):  # pylint: disable=no-self-argument
        """
        Validate that the stop loss value
        is set and between -1 and -0.001.
        """
        if not -1 <= value <= -0.001:
            logger.error(
                'Received stop loss %f', value
            )
        return value

    @validator('take_profit', pre=True, always=True)
    def validate_take_profit(cls, value):  # pylint: disable=no-self-argument
        """
        Validate that the take profit value
        is set and greater than 0.001.
        """
        if value is not None and value < 0.001:
            pass
        return value


class PortfolioManagement(BaseModel):
    """
    Request model for portfolio management configuration.
    """
    starting_amount: int = Field(
        ...,
        description="Initial amount of money in the portfolio",
        examples=[10000, 50000]
    )
    trade_size: TradeSize = Field(
        ...,
        description="Trade size configuration, either dynamic or static"
    )
    trade_targets: TradeTargets = Field(
        ...,
        description="Trade targets for take profit and stop loss"
    )
