"""
SignalService is responsible for managing and processing trading signals.
"""
import logging
from typing import Dict, List, Tuple, Union

import pandas as pd

from backtester.api.requests.trading_system import TradingSystemRules
from backtester.application.indicator_service import IndicatorService
from backtester.domain.enums.order_type import OrderType
from backtester.domain.enums.rule_comparison_method import RuleComparisonMethod
from backtester.domain.enums.rule_property_type import RulePropertyType
from backtester.domain.signals.group_rule import GroupRule
from backtester.domain.signals.indicator_registry import IndicatorRegistry
from backtester.domain.signals.order_type_rule import OrderTypeRule
from backtester.domain.signals.rule import Rule
from backtester.domain.signals.tile import Tile
from backtester.domain.signals.trading_sustem_rule import TradingSystemRule

logger = logging.getLogger(__name__)


class SignalService:
    """
    SignalService is responsible for managing and processing trading signals.
    """

    def __init__(
            self,
            indicator_service: IndicatorService,
            indicator_registry: IndicatorRegistry

    ):
        """
        Initializes the SignalService with an IndicatorClient.
        """
        self.indicator_service = indicator_service
        self.indicator_registry = indicator_registry
        self.price_columns = ['open', 'high', 'low', 'close']

    @staticmethod
    def _get_value_mask(tile: Tile) -> float:
        """
        Get the value mask for a tile of type VALUE.
        :param tile: Tile object containing the value mask.
        :return: The value mask as a float.
        """
        return tile.parameters.value

    def get_indicator_masks(
            self,
            ticker_data: pd.DataFrame,
            indicator_data: Dict
    ) -> Dict:
        """
        Calculate indicator masks for the given ticker data and indicator data.
        :param ticker_data: pd.DataFrame containing ticker data.
        :param indicator_data: Dict containing indicator data.
        :return: A dictionary of masks for each indicator.
        """
        logger.debug("Calculating indicator masks for ticker data.")
        masks = self.indicator_service.compute_masks(
            indicators=indicator_data,
            price_data={**ticker_data[self.price_columns].to_dict(orient='list')}
        )

        logger.debug("Indicator masks calculated successfully.")
        return masks

    @staticmethod
    def assign_indicator_masks(
            masks: Dict[str, List],
            indicators: Dict[str, Tile]
    ) -> None:
        """
        Assigns masks to indicators based on their tile IDs.
        :param masks: Calculated masks for indicators
        :param indicators: Dictionary of Tile objects representing indicators
        """
        for tile_id in masks.keys():
            mask = masks.get(tile_id)
            tile = indicators.get(tile_id)
            tile.set_mask(mask)
        logger.debug("Indicator masks assigned to tiles successfully.")

    @staticmethod
    def _get_indicator_mask(
            tile: Tile
    ) -> pd.Series:
        """
        Get the mask for a tile of type INDICATOR.
        :param tile: tile
        :return: The mask.
        """
        return tile.mask

    def _get_current_mask(
            self,
            tile: Tile
    ) -> Union[pd.Series, float]:
        """

        :param tile: Tile object containing the mask.
        :return: The mask for the tile, which can be a pandas Series or a float value.
        """
        if tile.type == RulePropertyType.INDICATOR:
            logger.debug(
                "Tile %s is of type INDICATOR,"
                " retrieving its mask.", tile
            )
            return self._get_indicator_mask(tile)
        logger.debug(
            "Tile %s is of type VALUE,"
            " retrieving its value mask.", tile
        )
        return self._get_value_mask(tile)

    @staticmethod
    def _get_previous_mask(
            mask: pd.Series,
            comparison_method: RuleComparisonMethod
    ) -> Union[pd.Series, None]:
        """
        Get the mask at the previous timestep to compare it against the current timestep.
        Applicable if the comparison method involves a cross.
        :param mask: mask at the current timestep
        :param comparison_method: Comparison method to determine if cross evaluation is needed.
        :return: The previous filter data as a pandas Series
         if comparison involves a cross; otherwise, None.
        """
        return mask.shift() if comparison_method.is_cross() else None

    def _get_tile_mask(
            self,
            tile: Tile,
            comparison_method: RuleComparisonMethod
    ) -> Tuple[pd.Series, Union[pd.Series, None]]:
        """
        Get the mask for a tile, including the current and previous masks if applicable.
        :param tile: Tile object containing the mask.
        :param comparison_method: Comparison method to determine if cross evaluation is needed.
        :return: A tuple containing the current mask and the previous mask (if applicable).
        """
        current_mask = self._get_current_mask(tile)
        logger.debug(
            "Current mask for tile %s: %s", tile, current_mask
        )
        previous_mask = self._get_previous_mask(current_mask, comparison_method)
        logger.debug(
            "Previous mask for tile %s: %s", tile, previous_mask
        )
        return current_mask, previous_mask

    def _get_rule_mask(
            self,
            rule: Rule
    ) -> None:
        """
        Get the mask for a rule by applying the comparison method to the first and second tiles.
        :param rule: Rule object containing the first and second tiles.
        """
        first_tile_mask = self._get_tile_mask(
            rule.first_tile,
            rule.comparison_method
        )
        logger.debug(
            "First tile mask for rule %s: %s", rule, first_tile_mask
        )

        second_tile_mask = self._get_tile_mask(
            rule.second_tile,
            rule.comparison_method
        )
        logger.debug(
            "Second tile mask for rule %s: %s", rule, second_tile_mask
        )

        rule_signals_mask = rule.comparison_method.apply(
            first_tile_mask,
            second_tile_mask
        )

        rule.signals.outer_merge(rule_signals_mask)

    def _get_group_rule_mask(
            self,
            group_rule: GroupRule
    ) -> None:
        """
        Get the mask for a group rule by iterating through its rules and merging their signals.
        :param group_rule: GroupRule object containing the rules.
        """
        for rule in group_rule.rules:
            self._get_rule_mask(
                rule
            )
            logger.debug(
                "Merged signals for rule %s: %s",
                rule,
                rule.signals.signal_indexes
            )
            group_rule.signals.outer_merge(rule.signals.signal_indexes)

    def _get_order_type_rule_mask(
            self,
            order_type_rule: OrderTypeRule
    ) -> None:
        """
        Get the mask for an order type rule
        by iterating through its group rules and merging their signals.
        :param order_type_rule: OrderTypeRule object containing the group rules.
        """
        for group_rule in order_type_rule.group_rules:
            self._get_group_rule_mask(
                group_rule=group_rule
            )
            logger.debug(
                "Merged signals for group rule %s: %s",
                group_rule,
                group_rule.signals.signal_indexes
            )
            order_type_rule.signals.inner_merge(
                group_rule.signals.signal_indexes
            )

    def get_trading_system_rule_mask(
            self,
            ticker_data: pd.DataFrame,
            trading_system_rule: TradingSystemRule
    ) -> pd.DataFrame:
        """
        Get the mask for a trading system rule
        by applying the order type rules to the ticker data.
        :param ticker_data: pd.DataFrame containing ticker data.
        :param trading_system_rule: TradingSystemRule object containing the order type rules.
        """
        self._get_order_type_rule_mask(
            order_type_rule=trading_system_rule.buy_rules
        )
        logger.debug(
            "Buy rules signals: %s",
            trading_system_rule.buy_rules
        )
        self._get_order_type_rule_mask(
            order_type_rule=trading_system_rule.sell_rules
        )
        logger.debug(
            "Sell rules signals: %s",
            trading_system_rule.sell_rules
        )

        if len(trading_system_rule.buy_rules) > 0:
            ticker_data.loc[
                trading_system_rule.buy_rules.signals.signal_indexes,
                'signal'] = OrderType.BUY

        if len(trading_system_rule.sell_rules) > 0:
            ticker_data.loc[
                trading_system_rule.sell_rules.signals.signal_indexes,
                'signal'] = OrderType.SELL

        ticker_data['signal'] = ticker_data['signal'].fillna(OrderType.NO_ACTION)
        logger.debug(
            "Final ticker data with signals: %s",
            ticker_data[['signal']]
        )
        return ticker_data

    def process_trading_system_rules(
            self,
            ticker_data: pd.DataFrame,
            trading_system_rules: TradingSystemRules,
    ) -> TradingSystemRule:
        """
        Processes the trading system rules to
         generate signals based on the provided ticker data.
        :param ticker_data: pd.DataFrame containing ticker data.
        :param trading_system_rules: TradingSystemRules containing the rules for the trading system.
        :return: TradingSystemRule instance containing the generated signals.
        """
        base_signal_indexes = ticker_data['date'].isnull()
        trading_system_signals = self._init_trading_system_signals(
            signal_indexes=base_signal_indexes,
            trading_system_rules=trading_system_rules,
            indicator_registry=self.indicator_registry
        )
        return trading_system_signals

    def calculate_indicators(
            self,
            ticker_data: pd.DataFrame,
    ) -> None:
        """
        Calculates indicators for the given ticker data
         and assigns them to the indicator registry.
        :param ticker_data: pd.DataFrame containing ticker data.
        """
        logger.debug("Calculating indicators for ticker data")
        masks = self.get_indicator_masks(
            ticker_data=ticker_data,
            indicator_data=self.indicator_registry.indicator_data
        )
        self.assign_indicator_masks(
            masks=masks,
            indicators=self.indicator_registry.indicators
        )

    def calculate_rules_mask(
            self,
            ticker_data: pd.DataFrame,
            trading_system_rule: TradingSystemRule
    ) -> pd.DataFrame:
        """
        Calculates the mask for the trading system rule
        :param ticker_data: pd.DataFrame containing ticker data.
        :param trading_system_rule: TradingSystemRule instance containing the rules to apply.
        :return: pd.DataFrame with the mask applied to the ticker data.
        """
        logger.debug(
            "Calculating rules mask for trading system rule %s",
            trading_system_rule
        )
        ticker_data = self.get_trading_system_rule_mask(
            ticker_data=ticker_data,
            trading_system_rule=trading_system_rule
        )
        return ticker_data

    @staticmethod
    def _init_trading_system_signals(
            signal_indexes: pd.Series,
            trading_system_rules: TradingSystemRules,
            indicator_registry: IndicatorRegistry
    ) -> TradingSystemRule:
        """
        Initializes a TradingSystemRule instance with the provided parameters.
        :param signal_indexes: pd.Series with signal indexes,
        :param trading_system_rules: TradingSystemRules,
        :param indicator_registry: IndicatorRegistry instance to manage indicators.
        :return: TradingSystemRule instance initialized with the provided parameters.
        """
        return TradingSystemRule(
            signal_indexes=signal_indexes,
            trading_system_rules=trading_system_rules,
            indicator_registry=indicator_registry
        )

    @staticmethod
    def _flatten_rules(
            strategy_signals
    ) -> List[Rule]:
        """
        Flattens the rules from the strategy signals into a single list.
        :param strategy_signals: TradingSystemRule instance containing buy and sell rules.
        :return: List of Rule instances from both buy and sell rules.
        """
        group_rules = (
                strategy_signals.buy_rules.group_rules +
                strategy_signals.sell_rules.group_rules
        )

        rules = []
        for rule in group_rules:
            rules += rule.rules
        return rules
