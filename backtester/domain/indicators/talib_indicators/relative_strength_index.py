"""
This module provides the implementation
for the Relative Strength Index(RSI) indicator.
"""
from typing import Dict, List

import numpy as np
import talib

from backtester.domain.indicators.indicator import Indicator
from backtester.domain.indicators.talib_indicator import TalibIndicator


@Indicator.register(name='RSI')
class RelativeStrengthIndex(TalibIndicator):
    """
       Computes the Relative Strength Index.

       Inherits:
           TalibIndicator: Provides
           preprocessing,
           validation,
           and postprocessing for TA-Lib indicator_subclasses.

       Methods:
           compute_talib_function(parameters: Dict)
           -> np.ndarray:
               Computes the RSI mask using the high,
               low,
               and close prices
               and the specified time period.

           get_required_parameters() -> list:
               Returns a list of required parameters for ADXR computation:
                ['Close', 'timeperiod'].
           """

    def _compute_talib_function(self, parameters: Dict) -> np.ndarray:
        """
        Unpack parameters and compute function
        """
        real = parameters.get('close')
        timeperiod = parameters.get('timeperiod')
        # pylint: disable=no-member
        mask = talib.RSI(
            real=real,
            timeperiod=timeperiod
        )
        return mask

    def _get_required_parameters(self) -> List:
        """
        Provide RSI's required parameters
        """
        return ['close', 'timeperiod']

    def __str__(self):
        return "Relative Strength Index"
