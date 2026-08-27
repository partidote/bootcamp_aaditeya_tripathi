"""
Stage 07: Reusable Outlier Detection and Handling Utilities.
"""

import pandas as pd
import numpy as np


def detect_outliers_iqr(series: pd.Series, k: float = 1.5) -> pd.Series:
    """
    Identify outliers using the Interquartile Range (IQR) rule.

    Parameters
    ----------
    series : pd.Series
        Numeric time series or distribution to evaluate.
    k : float, default=1.5
        IQR multiplier defining whisker boundaries (k > 0).

    Returns
    -------
    pd.Series
        Boolean Series where True indicates an outlier.
    """
    if series.empty:
        return pd.Series(dtype=bool, index=series.index)
    if k <= 0:
        raise ValueError("Multiplier k must be strictly positive.")

    clean_s = series.dropna()
    q1 = clean_s.quantile(0.25)
    q3 = clean_s.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - k * iqr
    upper_bound = q3 + k * iqr

    return (series < lower_bound) | (series > upper_bound)


def detect_outliers_zscore(series: pd.Series, threshold: float = 3.0, ddof: int = 1) -> pd.Series:
    """
    Identify outliers based on parametric Standard Z-Score.

    Parameters
    ----------
    series : pd.Series
        Numeric series to evaluate.
    threshold : float, default=3.0
        Standard deviation cutoff distance (|z| > threshold).
    ddof : int, default=1
        Degrees of freedom adjustment (ddof=1 for sample std).

    Returns
    -------
    pd.Series
        Boolean Series where True indicates an outlier.
    """
    if series.empty:
        return pd.Series(dtype=bool, index=series.index)
    if threshold <= 0:
        raise ValueError("Threshold must be strictly positive.")

    clean_s = series.dropna()
    mu = clean_s.mean()
    sigma = clean_s.std(ddof=ddof)

    if sigma == 0 or np.isnan(sigma):
        return pd.Series(False, index=series.index)

    z = (series - mu) / sigma
    return z.abs() > threshold


def winsorize_series(series: pd.Series, lower: float = 0.05, upper: float = 0.95) -> pd.Series:
    """
    Cap extreme values to specified lower and upper quantiles (Winsorization).

    Parameters
    ----------
    series : pd.Series
        Numeric series to adjust.
    lower : float, default=0.05
        Lower percentile threshold (0 <= lower < upper <= 1).
    upper : float, default=0.95
        Upper percentile threshold (0 <= lower < upper <= 1).

    Returns
    -------
    pd.Series
        Series with values clipped outside quantile boundaries.
    """
    if series.empty:
        return series.copy()
    if not (0.0 <= lower < upper <= 1.0):
        raise ValueError("Quantile bounds must satisfy 0 <= lower < upper <= 1.")

    lo_val = series.quantile(lower)
    hi_val = series.quantile(upper)
    return series.clip(lower=lo_val, upper=hi_val)
