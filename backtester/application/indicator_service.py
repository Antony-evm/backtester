import logging
from typing import Dict, List

from backtester.api.exceptions.indicator_exceptions import IndicatorNotFoundError
from backtester.application.indicator_validator_service import IndicatorValidatorService
from backtester.domain.indicators.indicator import Indicator
from backtester.domain.indicators.indicator_data import IndicatorData
from backtester.domain.indicators.talib_indicators import *

logger = logging.getLogger(__name__)


class IndicatorService:
    def __init__(
            self,
            indicator_validator_service: IndicatorValidatorService,
            registry: Dict
    ):
        self.registry = registry
        self.indicator_validator_service = indicator_validator_service
        self.indicator_masks = {}

    def compute_masks(
            self,
            indicators: Dict,
            price_data: Dict[str, List]
    ) -> Dict[str, List]:
        """
        Retrieve indicator func from Indicator Registry.
        Preprocess the parameters,
        compute the mask,
        and postprocess the result before you return it.
        """
        price_data = self.indicator_validator_service.convert_lists_to_numpy_arrays(
            price_data
        )
        for indicator_id in indicators.keys():
            self._compute_mask(
                indicators=indicators,
                indicator_id=indicator_id,
                price_data=price_data
            )

        return self.indicator_masks

    def _get_indicator_class(
            self,
            name: str
    ) -> Indicator:
        """
        Find an indicator by name.
        Using a registry allows us to map a string to a function.
        """
        indicator = self.registry.get(name)
        if not indicator:
            logger.error(
                "Indicator %s has not been implemented",
                name
            )
            raise IndicatorNotFoundError(
                indicator=name
            )
        return indicator()

    def _compute_mask(
            self,
            indicators: Dict[str, IndicatorData],
            price_data: Dict[str, List],
            indicator_id: str,
    ) -> None:
        indicator = indicators.get(indicator_id)
        name = indicator.get('name')
        parameters = indicator.get('parameters')
        parameters.update(price_data)
        # By importing all the declared indicator_subclasses
        # we are allowing them to be registered in the indicator class.
        indicator_function = self._get_indicator_class(name)
        logger.info(
            'Indicator %s initiated successfully from id: %s',
            name,
            indicator_id
        )
        mask = indicator_function.compute(parameters)
        logger.info(
            'Indicator mask computed successfully for %s',
            indicator_id
        )
        self.indicator_masks[indicator_id] = mask
