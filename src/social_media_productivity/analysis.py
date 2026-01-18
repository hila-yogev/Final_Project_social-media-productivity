# --------------- Statistical Analysis Module ---------------
# This module performs the statistical tests.

import pandas as pd
from scipy.stats import spearmanr, kruskal
from src.social_media_productivity.logger_config import setup_logger

logger = setup_logger()

import matplotlib.pyplot as plt
import pandas as pd

#  functions for descriptive and visual analysis of the dataset prior to statistical testing.
def plot_distributions_with_kde(df: pd.DataFrame) -> None:
    """
    Plot histograms with overlaid Kernel Density Estimation (KDE)
    for key continuous variables.

    This visualization helps assess:
    - Shape of the distribution
    - Skewness (left / right)
    - Presence of multiple modes
    - Deviations from normality

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataset used for analysis
    """

    variables = {
        "daily_social_media_time": "Daily Social Media Time (hours)",
        "perceived_productivity_score": "Perceived Productivity Score",
        "actual_productivity_score": "Actual Productivity Score",
        "productivity_gap": "Productivity Gap"
    }

    for col, title in variables.items():

        plt.figure()

        # Histogram (normalized to density)
        plt.hist(
            df[col],
            bins=30,
            density=True,
            alpha=0.6,
            label="Histogram"
        )

        # KDE curve
        df[col].plot(
            kind="kde",
            linewidth=2,
            label="KDE"
        )

        # Plot labels
        plt.title(f"Distribution of {title}")
        plt.xlabel(title)
        plt.ylabel("Density")
        plt.legend()

        plt.show()

def social_media_time_histogram(df: pd.DataFrame) -> tuple[float, float]:
    # displays social media time histogram.
    pass


def run_spearman_correlation(df: pd.DataFrame) -> tuple[float, float]:
    # Calculates Spearman correlation: Time vs Productivity Gap.
    var1, var2 = 'daily_social_media_time', 'productivity_gap'
    logger.info(f"Running Spearman Correlation: {var1} vs {var2}")

    corr, p_value = spearmanr(df[var1], df[var2])
    logger.info(f"Spearman Result: Correlation={corr:.4f}, p-value={p_value:.4f}")

    if p_value < 0.05:
        logger.info(">> Result is STATISTICALLY SIGNIFICANT.")
    else:
        logger.info(">> Result is NOT statistically significant.")
    return corr, p_value


def run_kruskal_wallis(df: pd.DataFrame) -> tuple[float, float]:
    #Performs Kruskal-Wallis test: Gap across Platforms.
    group_col, value_col = 'social_platform_preference', 'productivity_gap'
    logger.info(f"Running Kruskal-Wallis Test: {value_col} by {group_col}")

    platforms = df[group_col].unique()
    groups = [df[df[group_col] == p][value_col] for p in platforms]

    stat, p_value = kruskal(*groups)
    logger.info(f"Kruskal-Wallis Result: H-stat={stat:.4f}, p-value={p_value:.4f}")

    if p_value < 0.05:
        logger.info(">> Significant differences found between platforms.")
    else:
        logger.info(">> No significant difference found between platforms.")
    return stat, p_value


def run_analysis_pipeline(df: pd.DataFrame) -> dict:
    # Orchestrator function that runs all statistical tests.
    results = {}
    logger.info("--- Starting Statistical Analysis ---")

    corr, p_spearman = run_spearman_correlation(df)
    results['spearman'] = {'correlation': corr, 'p_value': p_spearman}

    stat, p_kruskal = run_kruskal_wallis(df)
    results['kruskal'] = {'statistic': stat, 'p_value': p_kruskal}

    logger.info("--- Statistical Analysis Complete ---")
    return results