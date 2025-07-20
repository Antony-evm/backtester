"""
All TaLib indicator_subclasses need to validate their results
and modify them to response appropriate outputs
"""
from typing import List

import numpy as np


class TalibConverter:
    """
    Ensures that the TaLib indicator_subclasses' outputs will have appropriate format
    """

    @staticmethod
    def convert_np_nan_to_none(result: np.ndarray) -> List:
        """
        Replace NaN values in a numpy array with None and return a list.
        np.NaN values are not json serialisable
        and cannot be returned
        Args:
            result (np.ndarray): Numpy array that may contain NaN values.
        Returns:
            list: List with NaN values replaced by None.
        """
        return [None if np.isnan(x) else x for x in result]
