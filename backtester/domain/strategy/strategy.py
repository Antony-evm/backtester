"""
Strategy entity for backtesting in the strategy service.
"""


from .trade import Trade
from backtester.api.requests.portfolio_management import PortfolioManagement, TradeSize, TradeTargets


class Strategy:
    """
    Represents a trading strategy for backtesting purposes.
    """

    def __init__(
            self,
            customer_id: str,
            portfolio_management: PortfolioManagement,
            request_id: str,
            trading_system_id: str
    ):
        """
        Initializes a Strategy instance.
        :param customer_id: customer identifier for the strategy.
        :param portfolio_management: Portfolio object containing initial amounts and trade settings.
        :param request_id: unique identifier for the backtesting request.
        :param trading_system_id: identifier for the trading system associated with the strategy.
        """
        self.trading_system_id = trading_system_id
        self.request_id = request_id
        self.customer_id = customer_id
        self.starting_amount = portfolio_management.starting_amount
        self.current_amount = portfolio_management.starting_amount
        self.trade_size: TradeSize = portfolio_management.trade_size
        self.trade_targets: TradeTargets = portfolio_management.trade_targets
        self.trades = 0
        self.wins = 0
        self.losses = 0
        self.all_trades = []

    @property
    def win_rate(self) -> float:
        """
        Calculates the win rate of the strategy.
        :return: win rate as a float rounded to 5 decimal places.
        """
        win_rate = 0
        if self.trades > 0:
            win_rate = self.wins / self.trades
        return round(win_rate, 5)

    @property
    def absolute_returns(self) -> float:
        """
        Calculates the absolute returns of the strategy.
        :return: absolute returns as a float rounded to 4 decimal places.
        """
        return round(self.current_amount - self.starting_amount, 4)

    @property
    def percentage_returns(self) -> float:
        """
        Calculates the percentage returns of the strategy.
        :return: percentage returns as a float rounded to 5 decimal places.
        """
        return round(self.current_amount / self.starting_amount, 5)

    def set_current_amount(self, amount: float) -> None:
        """
        Sets the current amount of the strategy.
        :param amount: the new current amount to set.
        """
        self.current_amount = amount

    def add_trade(self) -> None:
        """
        Increments the trade count for the strategy.
        """
        self.trades += 1

    def add_win(self) -> None:
        """
        Increments the win count for the strategy.
        """
        self.wins += 1

    def add_loss(self) -> None:
        """
        Increments the loss count for the strategy.
        """
        self.losses += 1

    def add_trade_object(self, trade: Trade) -> None:
        """
        Adds a Trade object to the strategy's list of trades.
        :param trade: Trade object to be added to the strategy.
        """
        self.all_trades.append(trade)

    def __repr__(self):
        """
        Returns a string representation of the Strategy instance.
        """
        return (
            f"Strategy(customer_id={self.customer_id}, "
            f"trading_system_id={self.trading_system_id}, "
            f"request_id={self.request_id}, "
            f"starting_amount={self.starting_amount}, "
            f"current_amount={self.current_amount}, "
            f"trade_size={self.trade_size}, "
            f"trade_targets={self.trade_targets}, "
            f"trades={self.trades}, "
            f"wins={self.wins}, "
            f"losses={self.losses})"
        )
