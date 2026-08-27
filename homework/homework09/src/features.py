"""
Stage 09: Reusable Feature Engineering Utilities.
"""

from typing import List, Optional
import pandas as pd
import numpy as np


def create_ratio_feature(df: pd.DataFrame, num_col: str, denom_col: str, new_col_name: str) -> pd.DataFrame:
    """
    Create a ratio feature between two numeric columns, handling zero-division.
    """
    df_out = df.copy()
    denom = df_out[denom_col].replace(0, np.nan)
    df_out[new_col_name] = df_out[num_col] / denom
    return df_out


def create_rolling_feature(df: pd.DataFrame, target_col: str, window: int = 3, func: str = 'mean', new_col_name: Optional[str] = None) -> pd.DataFrame:
    """
    Create rolling window statistics for temporal or sequential data.
    """
    df_out = df.copy()
    if new_col_name is None:
        new_col_name = f"{target_col}_rolling_{func}_{window}"
    
    if func == 'mean':
        df_out[new_col_name] = df_out[target_col].rolling(window=window, min_periods=1).mean()
    elif func == 'std':
        df_out[new_col_name] = df_out[target_col].rolling(window=window, min_periods=1).std().fillna(0)
    else:
        raise ValueError(f"Unsupported func: {func}")
        
    return df_out


def encode_categorical(df: pd.DataFrame, col: str, method: str = 'onehot') -> pd.DataFrame:
    """
    Encode a categorical column using one-hot, label, or frequency encoding.
    """
    df_out = df.copy()
    if method == 'onehot':
        df_out = pd.get_dummies(df_out, columns=[col], prefix=col, drop_first=False)
    elif method == 'label':
        df_out[f"{col}_encoded"] = df_out[col].astype('category').cat.codes
    elif method == 'frequency':
        freq_map = df_out[col].value_counts(normalize=True).to_dict()
        df_out[f"{col}_freq"] = df_out[col].map(freq_map)
    else:
        raise ValueError(f"Unsupported encoding method: {method}. Choose 'onehot', 'label', or 'frequency'.")
    return df_out
