"""
This module defines the Portfolio Management part of the trading system request
"""
import logging
from typing import Optional

from backtesting_io_manager.exceptions.strategy_exceptions import (
    InvalidStopLoss, InvalidTakeProfit)
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)


class TradeSize(BaseModel):
    """
    Request model for trade size configuration.
    """
    type: str = Field(
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

    @field_validator("stop_loss")
    def validate_stop_loss(cls, value):  # pylint: disable=no-self-argument
        """
        Validate that the stop loss value
        is set and between -1 and -0.001.
        """
        if not -1 <= value <= -0.001:
            logger.error(
                'Received stop loss %f', value
            )
            raise InvalidStopLoss(value)
        return value

    @field_validator("take_profit")
    def validate_take_profit(cls, value):  # pylint: disable=no-self-argument
        """
        Validate that the take profit value
        is set and greater than 0.001.
        """
        if value is not None and value < 0.001:
            raise InvalidTakeProfit(value)
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
