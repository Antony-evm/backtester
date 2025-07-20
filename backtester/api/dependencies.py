from fastapi import Depends

from backtester.application.backtester import Backtester
from backtester.application.indicator_service import IndicatorService
from backtester.application.indicator_validator_service import IndicatorValidatorService
from backtester.application.signal_service import SignalService
from backtester.application.strategy_service import StrategyService
from backtester.application.ticker_service import TickerService
from backtester.application.trade_service import TradeService
from backtester.domain.indicators.indicator import Indicator
from backtester.domain.signals.indicator_registry import IndicatorRegistry
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


def init_strategy_service() -> StrategyService:
    return StrategyService()


def init_trade_service() -> TradeService:
    return TradeService()


def init_indicator_validator_service(
) -> IndicatorValidatorService:
    return IndicatorValidatorService()


def init_indicator_service(
        indicator_validator_service: IndicatorValidatorService = Depends(init_indicator_validator_service)
) -> IndicatorService:
    """
    Initialize the IndicatorService with the given registry.
    Defaults to using the global Indicator.registry.
    """
    return IndicatorService(
        indicator_validator_service=indicator_validator_service,
        registry=Indicator.registry
    )


def init_indicator_registry() -> IndicatorRegistry:
    """
    Initializes the IndicatorRegistry.
    """
    return IndicatorRegistry()


def init_signal_service(
        indicator_registry: IndicatorRegistry = Depends(init_indicator_registry),
        indicator_service: IndicatorService = Depends(init_indicator_service)
) -> SignalService:
    return SignalService(
        indicator_registry=indicator_registry,
        indicator_service=indicator_service
    )


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
