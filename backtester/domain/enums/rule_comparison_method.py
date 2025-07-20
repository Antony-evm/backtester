"""
This module defines the RuleComparisonMethod enum,
 which specifies various methods for comparing values in trading strategies.
"""
from enum import Enum


class RuleComparisonMethod(Enum):
    """
    Enum representing comparison methods for trading rules.
    """
    IS_ABOVE = 'IS_ABOVE'
    IS_BELOW = 'IS_BELOW'
    CROSSES_ABOVE = 'CROSSES_ABOVE'
    CROSSES_BELOW = 'CROSSES_BELOW'

    def is_cross(self) -> bool:
        """
        Checks if the comparison method is a cross type.
        :return: True if the method is a cross type, False otherwise.
        """
        return self in {
            RuleComparisonMethod.CROSSES_ABOVE,
            RuleComparisonMethod.CROSSES_BELOW
        }

    def apply(self, f, s) -> bool:
        """
        Applies the comparison method to the given inputs.

        :param f: A tuple of floats representing the first value and its previous state.
        :param s: A tuple of floats representing the second value and its previous state.
        :return: The result of the comparison.
        """
        if self == RuleComparisonMethod.IS_ABOVE:
            result = f[0] > s[0]
        elif self == RuleComparisonMethod.IS_BELOW:
            result = f[0] < s[0]
        elif self == RuleComparisonMethod.CROSSES_ABOVE:
            result = (f[0] > s[0]) & (f[1] < s[1])
        elif self == RuleComparisonMethod.CROSSES_BELOW:
            result = (f[0] < s[0]) & (f[1] > s[1])
        return result