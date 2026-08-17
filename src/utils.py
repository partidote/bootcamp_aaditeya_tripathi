import pandas as pd

def get_summary_stats(df: pd.DataFrame, group_col: str = "category", target_col: str = "value") -> pd.DataFrame:
    """Compute aggregated statistics for a specified column grouped by category."""
    return df.groupby(group_col)[target_col].agg(["count", "mean", "std", "sum", "min", "max"])
