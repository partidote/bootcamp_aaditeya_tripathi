"""
Stage 06: Reusable Data Preprocessing and Cleaning Functions.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def fill_missing_median(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Impute missing values with column medians for numeric fields.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list of str, optional): Specific numeric columns to impute.
                                     Defaults to all numeric columns.

    Returns:
    pd.DataFrame: A copy of DataFrame with missing values filled.
    """
    df_copy = df.copy()
    if columns is None:
        columns = list(df_copy.select_dtypes(include=np.number).columns)
    for col in columns:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy


def drop_missing(df: pd.DataFrame, columns: Optional[List[str]] = None, threshold: Optional[float] = None) -> pd.DataFrame:
    """
    Drop rows based on missing column values or completeness threshold.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list of str, optional): Subset of columns to evaluate for missingness.
    threshold (float, optional): Fraction (0.0 to 1.0) of non-null columns required per row.

    Returns:
    pd.DataFrame: A copy of DataFrame with specified missing rows dropped.
    """
    df_copy = df.copy()
    if columns is not None:
        return df_copy.dropna(subset=columns)
    if threshold is not None:
        # thresh expects an integer count of non-null values required
        min_count = int(threshold * df_copy.shape[1])
        return df_copy.dropna(thresh=min_count)
    return df_copy.dropna()


def normalize_data(df: pd.DataFrame, columns: Optional[List[str]] = None, method: str = 'minmax') -> pd.DataFrame:
    """
    Scale numeric features using MinMaxScaler or StandardScaler.

    Parameters:
    df (pd.DataFrame): Input DataFrame.
    columns (list of str, optional): Numeric columns to scale. Defaults to all numeric columns.
    method (str): Scaling method ('minmax' or 'standard'). Defaults to 'minmax'.

    Returns:
    pd.DataFrame: A copy of DataFrame with scaled columns.
    """
    df_copy = df.copy()
    if columns is None:
        columns = list(df_copy.select_dtypes(include=np.number).columns)
    
    if method.lower() == 'minmax':
        scaler = MinMaxScaler()
    elif method.lower() == 'standard':
        scaler = StandardScaler()
    else:
        raise ValueError(f"Unsupported method: {method}. Choose 'minmax' or 'standard'.")

    if len(columns) > 0:
        df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy
