"""
Implement framework for Talib Indicators
"""
import abc
import logging
from abc import abstractmethod
from typing import Any, Dict, List

import numpy as np

from backtester.application.talib_converter import TalibConverter
from backtester.domain.indicators.indicator import Indicator

logger = logging.getLogger(__name__)


class TalibIndicator(Indicator, abc.ABC):

    def compute(
            self,
            parameters: Dict[str, Any]
    ) -> List:

        self._validate_parameters(parameters)
        try:
            mask = self._compute_talib_function(parameters)
            mask = self._postprocess(mask)
            return mask
        except Exception as error:
            logger.error(
                "Encountered unexpected error calculating %s."
                " Error: %s",
                str(self),
                error
            )
            raise IndicatorComputationError(
                indicator=str(self)
            ) from error

    @staticmethod
    def _postprocess(
            output: np.ndarray
    ) -> List:
        result = TalibConverter.convert_np_nan_to_none(output)
        return result

    def _validate_parameters(self, parameters: Dict[str, Any]) -> None:
        """
        Validate that all required parameters are present and not None.
        """
        missing_parameters = [
            p for p in self._get_required_parameters() if parameters.get(p) is None
        ]
        if missing_parameters:
            logger.error(
                "Critical parameters are missing to calculate indicator %s"
                " Missing parameters: %s",
                str(self),
                missing_parameters
            )
            raise MissingIndicatorParametersError(
                indicator=str(self),
                missing_parameters=missing_parameters
            )

    @abstractmethod
    def _get_required_parameters(self) -> List[str]:
        """
        Subclasses must specify the required parameters for their specific indicator.
        """

    @abstractmethod
    def _compute_talib_function(self, parameters: Dict[str, Any]) -> np.ndarray:
        """
        Subclasses must specify which TA-Lib function to call and how to map the parameters.
        """

