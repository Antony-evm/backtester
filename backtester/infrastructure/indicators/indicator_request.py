"""
This module defines the IndicatorRequest
"""
from typing import Dict

from pydantic import BaseModel


class IndicatorRequest(BaseModel):
    """
    Represents a request for indicators and price data.
    """
    indicators: Dict
    price_data: Dict
