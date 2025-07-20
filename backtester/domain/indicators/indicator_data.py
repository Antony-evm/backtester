from typing import Dict

from pydantic import BaseModel


class IndicatorData(BaseModel):
    """
    Base structure of each indicator requested
    """
    name: str
    parameters: Dict
