from fastapi import Depends

from backtester.application.backtester import Backtester
from backtester.application.signal_service import SignalService
from backtester.application.ticker_service import TickerService
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


def init_backtester(
        ticker_service: TickerService = Depends(init_ticker_service),
        signal_service: SignalService = Depends(init_signal_service)
):
    return Backtester(
        ticker_service=ticker_service,
        signal_service=signal_service
    )
