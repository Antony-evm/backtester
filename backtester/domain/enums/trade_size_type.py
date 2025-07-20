"""
Trade Size Type Enum
"""
from enum import Enum


class TradeSizeType(Enum):
    """
    Enum representing the type of trade size.
    """
    DYNAMIC = 'DYNAMIC'
    STATIC = 'STATIC'
