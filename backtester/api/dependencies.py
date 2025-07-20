from fastapi import Depends

from backtester.application.backtester import Backtester
from backtester.application.signal_service import SignalService
from backtester.application.strategy_service import StrategyService
from backtester.application.ticker_service import TickerService
from backtester.application.trade_service import TradeService
from backtester.infrastructure.ticker_provider import TickerProvider


def init_ticker_provider(
):
    return TickerProvider()


def init_ticker_service(
        ticker_provider: TickerProvider = Depends(init_ticker_provider)
):
    return TickerService(
        ticker_provider=ticker_provider
    )


def init_signal_service(
) -> SignalService:
    return SignalService()


def init_strategy_service() -> StrategyService:
    return StrategyService()


def init_trade_service() -> TradeService:
    return TradeService()


def init_backtester(
        ticker_service: TickerService = Depends(init_ticker_service),
        signal_service: SignalService = Depends(init_signal_service),
        strategy_service: StrategyService = Depends(init_strategy_service),
        trade_service: TradeService = Depends(init_trade_service)
) -> Backtester:
    return Backtester(
        ticker_service=ticker_service,
        signal_service=signal_service,
        strategy_service=strategy_service,
        trade_service=trade_service
    )
