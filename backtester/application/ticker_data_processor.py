"""
Ticker Data Processor
"""
import numpy as np
import pandas as pd


class TickerDataProcessor:
    """
    A class to process ticker data for trading strategies.
    """

    @staticmethod
    def add_helper_columns(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add helper columns to the DataFrame.
        """
        df['previous_close'] = df['close'].shift(1)

        # Calculate returns from same day's open, to be used for first trading period
        df['returns_on_close_same_day'] = (
                (df['close'] - df['open']) / df['open']
        ).astype(float)
        # Calculate returns from previous day's close for the rest of the trading periods
        df['returns_on_close'] = (
                (df['close'] - df['previous_close']) / df['previous_close']
        ).astype(float)
        # Calculate returns for current trading period's high and low to identify hitting TP or SL
        # during the first trading period
        df['returns_on_high_same_day'] = (
                (df['high'] - df['open']) / df['open']
        ).astype(float)
        df['returns_on_low_same_day'] = (
                (df['low'] - df['open']) / df['open']
        ).astype(float)

        # Calculate returns from previous day's high and low to identify hitting TP or SL
        df['returns_on_high'] = (
                (df['high'] - df['previous_close']) / df['previous_close']
        ).astype(float)

        df['returns_on_low'] = (
                (df['low'] - df['previous_close']) / df['previous_close']
        ).astype(float)

        df = df.drop(['previous_close'], axis=1)

        df = df.replace({np.nan: 0, np.inf: 0})

        df['signal'] = None

        return df

    @staticmethod
    def convert_date_to_isoformat(df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert date column in DataFrame to ISO format.
        :param df: dataframe with date column to be converted
        :return: dataframe with date column in ISO format
        """
        df['date'] = df['date'].apply(
            lambda dt: dt.isoformat() if pd.notnull(dt) else None
        )
        return df
