"""
Stage 08: Reusable Exploratory Data Analysis (EDA) Utilities.
"""

from typing import Optional
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis


def eda_summary(df: pd.DataFrame, missing_thresh: float = 0.2, high_cardinality_thresh: int = 50) -> pd.DataFrame:
    """
    Generate a comprehensive profile of numeric and categorical columns,
    flagging potential issues for downstream feature engineering (Stage 09).

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to profile.
    missing_thresh : float, default=0.2
        Threshold proportion above which missingness is flagged.
    high_cardinality_thresh : int, default=50
        Threshold above which non-numeric cardinality is flagged.

    Returns
    -------
    pd.DataFrame
        Summary table indexed by column name.
    """
    summary_data = []

    for col in df.columns:
        series = df[col]
        n_missing = series.isna().sum()
        pct_missing = n_missing / len(df)
        dtype = str(series.dtype)
        unique_count = series.nunique(dropna=True)
        
        # Flags
        flags = []
        if pct_missing > missing_thresh:
            flags.append(f"High Missing ({pct_missing:.1%})")
        
        col_info = {
            'column': col,
            'dtype': dtype,
            'missing_count': n_missing,
            'missing_pct': round(pct_missing, 3),
            'unique_count': unique_count,
            'mean': np.nan,
            'std': np.nan,
            'median': np.nan,
            'skew': np.nan,
            'kurtosis': np.nan,
            'top_val_share': np.nan,
            'flags': ''
        }

        # Profile numeric
        if pd.api.types.is_numeric_dtype(series):
            clean_s = series.dropna()
            if len(clean_s) > 0:
                col_info['mean'] = round(clean_s.mean(), 3)
                col_info['std'] = round(clean_s.std(), 3)
                col_info['median'] = round(clean_s.median(), 3)
                if len(clean_s) > 2:
                    col_info['skew'] = round(float(skew(clean_s)), 3)
                    col_info['kurtosis'] = round(float(kurtosis(clean_s)), 3)
                if clean_s.std() == 0:
                    flags.append("Near-Zero Variance")
        else:
            # Profile non-numeric / categorical
            top_freq = series.value_counts(normalize=True, dropna=True)
            if not top_freq.empty:
                col_info['top_val_share'] = round(top_freq.iloc[0], 3)
                if top_freq.iloc[0] > 0.85:
                    flags.append("Dominant Category (>85%)")
            if unique_count > high_cardinality_thresh:
                flags.append("High Cardinality")

        col_info['flags'] = ", ".join(flags) if flags else "OK"
        summary_data.append(col_info)

    return pd.DataFrame(summary_data).set_index('column')
