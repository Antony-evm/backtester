"""
Thresholds entity for backtesting strategies.
"""


class Thresholds:
    """Represents thresholds for backtesting strategies."""

    def __init__(
            self,
            upper: float,
            lower: float
    ):
        """
        Initializes a Thresholds instance.
        :param upper: Upper threshold value for the strategy.
        :param lower: Lower threshold value for the strategy.
        """
        self.upper = upper
        self.lower = lower
