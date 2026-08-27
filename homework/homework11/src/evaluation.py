"""
Stage 11: Evaluation & Risk Communication Utilities.
"""

import numpy as np
import pandas as pd


def mean_impute(a: np.ndarray) -> np.ndarray:
    """Impute missing values using column/array mean."""
    m = np.nanmean(a)
    out = a.copy()
    out[np.isnan(out)] = m
    return out


def median_impute(a: np.ndarray) -> np.ndarray:
    """Impute missing values using column/array median."""
    m = np.nanmedian(a)
    out = a.copy()
    out[np.isnan(out)] = m
    return out


class SimpleLinReg:
    """Lightweight 1D OLS Linear Regression."""
    def fit(self, X, y):
        X1 = np.c_[np.ones(len(X)), X.ravel()]
        beta = np.linalg.pinv(X1) @ y
        self.intercept_, self.coef_ = float(beta[0]), np.array([float(beta[1])])
        return self

    def predict(self, X):
        return self.intercept_ + self.coef_[0] * X.ravel()


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Mean Absolute Error."""
    return float(np.mean(np.abs(y_true - y_pred)))


def bootstrap_metric(y_true, y_pred, fn=mae, n_boot=600, seed=111, alpha=0.05):
    """Estimate empirical confidence interval for a chosen evaluation metric."""
    rng = np.random.default_rng(seed)
    idx = np.arange(len(y_true))
    stats = []
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        stats.append(fn(y_true[b], y_pred[b]))
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {'mean': float(np.mean(stats)), 'lo': float(lo), 'hi': float(hi)}


def bootstrap_predictions(X, y, x_grid, fit_fn, n_boot=600, seed=111, alpha=0.05):
    """Bootstrap regression fit lines across an evaluation grid to generate CI bands."""
    rng = np.random.default_rng(seed)
    preds = []
    idx = np.arange(len(y))
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        m = fit_fn(X[b].reshape(-1, 1), y[b])
        preds.append(m.predict(x_grid))
    P = np.vstack(preds)
    return P.mean(axis=0), np.percentile(P, 100 * alpha / 2, axis=0), np.percentile(P, 100 * (1 - alpha / 2), axis=0)
