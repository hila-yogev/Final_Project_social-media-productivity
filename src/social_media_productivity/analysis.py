"""
analysis.py

Statistical analysis for the project:
1) Spearman correlations between daily social media time and:
   - productivity gap (perceived - actual)
   - actual productivity score
   - perceived productivity score
2) Kruskal-Wallis test comparing productivity gap across preferred platforms

All outputs are written to the project logger.
"""

from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr, kruskal

from src.social_media_productivity.logger_config import setup_logger
from src.social_media_productivity.constants import (
    ALPHA,
    COL_TIME,
    COL_GAP,
    COL_ACTUAL,
    COL_PERCEIVED,
    COL_PLATFORM,
)

logger = setup_logger()


def _run_single_spearman(df: pd.DataFrame, x_col: str, y_col: str) -> tuple[float, float]:
    """
    Run Spearman correlation between two columns and log the result.

    Parameters
    ----------
    df:
        Input dataframe.
    x_col, y_col:
        Column names for the two variables.

    Returns
    -------
    (rho, p_value):
        Spearman correlation coefficient (rho) and p-value.
    """
    logger.info(f"Running Spearman Correlation: {x_col} vs {y_col}")

    # Spearman cannot handle NaNs reliably -> drop rows missing either variable.
    pair_df = df[[x_col, y_col]].dropna()

    # Edge case: if data is too small, spearmanr can return nan or error.
    if len(pair_df) < 3:
        logger.warning(
            f"Not enough valid rows for Spearman ({x_col} vs {y_col}). "
            f"Need >= 3, got {len(pair_df)}."
        )
        return float("nan"), float("nan")

    rho, p_value = spearmanr(pair_df[x_col], pair_df[y_col])

    logger.info(f"   Result: rho={rho:.4f}, p-value={p_value:.4f}")

    if p_value < ALPHA:
        logger.info(f"   >> SIGNIFICANT (p < {ALPHA}).")
    else:
        logger.info(f"   >> Not significant (p >= {ALPHA}).")

    return float(rho), float(p_value)


def run_correlation_suite(df: pd.DataFrame) -> dict[str, tuple[float, float]]:
    """
    Run the project's 3 Spearman correlations.

    1) Time vs Gap (original hypothesis)
    2) Time vs Actual Productivity
    3) Time vs Perceived Productivity

    Returns
    -------
    dict:
        Mapping from test name to (rho, p_value).
    """
    logger.info("--- Starting Correlation Suite ---")

    results: dict[str, tuple[float, float]] = {}

    results["gap"] = _run_single_spearman(df, COL_TIME, COL_GAP)
    results["actual"] = _run_single_spearman(df, COL_TIME, COL_ACTUAL)
    results["perceived"] = _run_single_spearman(df, COL_TIME, COL_PERCEIVED)

    return results


def run_kruskal_wallis(df: pd.DataFrame) -> tuple[float, float]:
    """
    Run Kruskal-Wallis test: Does productivity gap differ across platform groups?

    Returns
    -------
    (h_stat, p_value)
    """
    logger.info(f"Running Kruskal-Wallis Test: {COL_GAP} by {COL_PLATFORM}")

    # Drop rows missing platform or gap
    kw_df = df[[COL_PLATFORM, COL_GAP]].dropna()

    # Build groups (one series per platform)
    platforms = kw_df[COL_PLATFORM].unique()

    groups = [kw_df.loc[kw_df[COL_PLATFORM] == p, COL_GAP] for p in platforms]

    # Kruskal needs at least 2 groups, and each group needs at least 1 value
    non_empty_groups = [g for g in groups if len(g) > 0]
    if len(non_empty_groups) < 2:
        logger.warning("Not enough non-empty platform groups for Kruskal-Wallis.")
        return float("nan"), float("nan")

    h_stat, p_value = kruskal(*non_empty_groups)

    logger.info(f"Kruskal-Wallis Result: H-stat={h_stat:.4f}, p-value={p_value:.4f}")

    if p_value < ALPHA:
        logger.info(">> Significant differences found between platforms.")
    else:
        logger.info(">> No significant difference found between platforms.")

    return float(h_stat), float(p_value)


def run_analysis_pipeline(df: pd.DataFrame) -> None:
    """
    Orchestrator function: runs all statistical tests in the correct order.
    """
    logger.info("--- Starting Statistical Analysis ---")

    run_correlation_suite(df)
    run_kruskal_wallis(df)

    logger.info("--- Statistical Analysis Complete ---")
