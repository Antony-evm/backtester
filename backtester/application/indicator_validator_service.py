"""
All TaLib indicator_subclasses need to validate their results
and modify them to response appropriate outputs
"""
from typing import Any, Dict

import numpy as np


class IndicatorValidatorService:
    """
    Ensures that the indicator_subclasses' outputs will have appropriate format
    """

    @staticmethod
    def convert_lists_to_numpy_arrays(parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Indicator parameters that are related to price directly, are received as lists.
        To compute masks, they need to be numpy arrays.
        Args:
            parameters (dict): Dictionary containing indicator parameters.

        Returns:
            dict: New dictionary with lists converted to numpy arrays where applicable.
        """
        numpy_parameters = {}
        for parameter, value in parameters.items():
            if isinstance(value, list):
                numpy_parameters[parameter] = np.array(value)
            else:
                numpy_parameters[parameter] = value
        return numpy_parameters

