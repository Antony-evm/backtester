from abc import ABC, abstractmethod
from typing import Any, Dict


class Indicator(ABC):
    """
    Base class for all talib_indicators.
    All indicator_subclasses should be able to:
     - bring the input to the relevant format
     - compute their mask
     - process the result to a JSON serialisable format
    """
    registry = {}

    @classmethod
    def register(cls, name: str):
        """
        Decorator to register an indicator class with a specific name.
        This is used to map indicator names to functions.
        """

        def wrapper(subclass):
            cls.registry[name] = subclass
            return subclass

        return wrapper

    @abstractmethod
    def compute(
            self,
            parameters: Dict[str, Any]
    ):
        """
        Abstract method to calculate the indicator mask.
        Must be implemented by subclasses.
        """