import logging
from typing import Dict



from backtester.domain.indicators.talib_indicators import *

logger = logging.getLogger(__name__)


class IndicatorService:
    def __init__(
            self,
            output_conversion_service: OutputConversionService,
            registry: Dict
    ):
        self.registry = registry
        self.validator_service = output_conversion_service
        self.indicator_masks = {}

    def compute_masks(
            self,
            indicator_request: IndicatorRequest
    ) -> IndicatorResponse:
        """
        Retrieve indicator func from Indicator Registry.
        Preprocess the parameters,
        compute the mask,
        and postprocess the result before you return it.
        """
        price_data = self.validator_service.convert_lists_to_numpy_arrays(
            indicator_request.price_data
        )
        for indicator_id in indicator_request.indicators.keys():
            self._compute_mask(
                indicator_request=indicator_request,
                indicator_id=indicator_id,
                price_data=price_data
            )

        return IndicatorResponse(
            indicator_masks=self.indicator_masks
        )

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
            indicator_request: IndicatorRequest,
            indicator_id: str,
            price_data: Dict
    ) -> None:
        indicator = indicator_request.indicators.get(indicator_id)
        name = indicator.name
        parameters = indicator.parameters
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
