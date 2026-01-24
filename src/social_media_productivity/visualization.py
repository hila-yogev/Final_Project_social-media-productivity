# --------------- Visualization Module ---------------
# This module generates and saves all project figures to outputs/figures/.

"""
Figures produced:
1) Histograms + KDE for key variables (with mean + median lines)
2) Scatter/regression plots (time vs gap / actual / perceived)
3) Boxplot: productivity gap by preferred platform

All saves are logged via the project logger.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.social_media_productivity.logger_config import setup_logger
from src.social_media_productivity.constants import (
    FIGURES_DIR,
    COL_TIME,
    COL_PERCEIVED,
    COL_ACTUAL,
    COL_GAP,
    COL_PLATFORM,
)

logger = setup_logger()


# Helper functions - private

def _ensure_output_dir(output_dir: Path = FIGURES_DIR) -> Path:
    """
    Ensure the output directory exists.

    Parameters
    ----------
    output_dir:
        Directory where figures will be saved.

    Returns
    -------
    Path
        The same directory path, guaranteed to exist.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def _save_figure(output_path: Path) -> None:
    """
    Save the current matplotlib figure and close it.

    Why this helper exists:
    - Centralizes save settings (dpi, tight layout)
    - Prevents memory leaks by always closing figures

    Parameters
    ----------
    output_path:
        Full path (including filename) where the figure is saved.
    """
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    logger.info(f"Saved figure: {output_path.name}")


# Public functions:

def plot_distributions_with_kde(df: pd.DataFrame) -> None:
    """
    Plot histograms with KDE for key variables and save them as PNG files.

    For each variable, if the column exists, we generate:
    - Histogram
    - KDE curve (density)
    """
    logger.info("Generating distribution plots (hist + KDE)...")
    save_dir = _ensure_output_dir()

    variables = [COL_TIME, COL_PERCEIVED, COL_ACTUAL, COL_GAP]

    for col in variables:
        if col not in df.columns:
            logger.warning(f"Skipping distribution plot. Missing column: '{col}'")
            continue

        # Get data and calculate statistics
        series = df[col].dropna()
        mean_val = series.mean()
        median_val = series.median()

        # Log the statistics
        logger.info(f"Distribution statistics for '{col}': mean={mean_val:.2f}, median={median_val:.2f}")

        plt.figure(figsize=(8, 6))
        sns.histplot(series, kde=True, stat="density", linewidth=0)
        plt.title(f"Distribution of {col.replace('_', ' ').title()}")
        plt.xlabel(col.replace("_", " ").title())
        plt.ylabel("Density")

        # Add text box with statistics
        textstr = f'Mean: {mean_val:.2f}\nMedian: {median_val:.2f}'
        plt.text(
            0.95, 0.95,  # Position: x=0.95 (right), y=0.95 (top) in axes coordinates
            textstr,
            transform=plt.gca().transAxes,  # Use axes coordinates (0-1 scale)
            fontsize=10,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)  # Box styling
        )
        
        output_file = save_dir / f"distribution_{col}.png"
        _save_figure(output_file)

    logger.info("Finished distribution plots.")

def plot_scatter_suite(df: pd.DataFrame) -> None:
    """
    Generates 4 scatter + heatmap plots:
    1) Actual Productivity vs Perceived Productivity
    2) Social Media Time vs Actual Productivity
    3) Social Media Time vs Perceived Productivity
    4) Social Media Time vs Gap
    """
    logger.info("Generating scatter + heatmap suite...")
    save_dir = _ensure_output_dir()

    relationships = [
        (COL_ACTUAL, COL_PERCEIVED, "Actual vs Perceived Productivity"),
        (COL_TIME, COL_ACTUAL, "Time vs Actual Productivity"),
        (COL_TIME, COL_PERCEIVED, "Time vs Perceived Productivity"),
        (COL_TIME, COL_GAP, "Time vs Gap"),
    ]

    for x_col, y_col, title in relationships:
        if x_col not in df.columns or y_col not in df.columns:
            logger.warning(
                f"Skipping scatter plot '{title}'. Missing column(s): "
                f"{[c for c in [x_col, y_col] if c not in df.columns]}"
            )
            continue

        plot_df = df[[x_col, y_col]].dropna()
        if plot_df.empty:
            logger.warning(f"Skipping scatter plot '{title}'. No valid (non-NaN) rows.")
            continue

        # Create figure with 2 subplots (1 row, 2 columns)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # LEFT SUBPLOT: Scatter plot with regression line
        sns.regplot(
            data=plot_df,
            x=x_col,
            y=y_col,
            scatter_kws={"alpha": 0.4},
            line_kws={"color": "red", "linewidth": 2},
            ax=ax1
        )

        ax1.set_title(f"{title} - Scatter Plot")
        ax1.set_xlabel(x_col.replace("_", " ").title())
        ax1.set_ylabel(y_col.replace("_", " ").title())
        
        # RIGHT SUBPLOT: Hexbin heatmap
        hexbin = ax2.hexbin(
            plot_df[x_col],
            plot_df[y_col],
            gridsize=20,
            cmap='YlOrRd',
            mincnt=1
        )
        plt.colorbar(hexbin, ax=ax2, label='Count')
        ax2.set_title(f"{title} - Heatmap")
        ax2.set_xlabel(x_col.replace("_", " ").title())
        ax2.set_ylabel(y_col.replace("_", " ").title())

        # Save this combined figure
        filename = f"scatter_&_heatmap_{x_col}_vs_{y_col}.png"
        output_file = save_dir / filename
        _save_figure(output_file)

    logger.info("Finished scatter plot suite.")


def plot_platform_comparison(df: pd.DataFrame) -> None:
    """
    Boxplot: Productivity Gap distribution by preferred social platform.
    """
    logger.info("Generating platform comparison box plot...")
    save_dir = _ensure_output_dir()

    if COL_PLATFORM not in df.columns or COL_GAP not in df.columns:
        logger.warning(
            f"Skipping platform boxplot. Missing column(s): "
            f"{[c for c in [COL_PLATFORM, COL_GAP] if c not in df.columns]}"
        )
        return

    plot_df = df[[COL_PLATFORM, COL_GAP]].dropna()
    if plot_df.empty:
        logger.warning("Skipping platform boxplot. No valid (non-NaN) rows.")
        return

    plt.figure(figsize=(12, 6))
    sns.boxplot(
        data=plot_df,
        x=COL_PLATFORM,
        y=COL_GAP,
        hue=COL_PLATFORM,      # Different color per platform
        palette="Set2",         # Soft pastel colors
        legend=False            # Hide redundant legend
    )

    plt.title("Productivity Gap Distribution by Platform")
    plt.xlabel("Preferred Social Media Platform")
    plt.ylabel("Productivity Gap")

    output_file = save_dir / "platform_boxplot.png"
    _save_figure(output_file)


def generate_visualizations(df: pd.DataFrame) -> None:
    """
    Orchestrator: runs all visualization functions in the intended order.
    """
    logger.info("--- Starting Visualization Pipeline ---")

    # Set global plot style (one place, consistent across all charts)
    sns.set_theme(style="whitegrid")

    plot_distributions_with_kde(df)
    plot_scatter_suite(df)
    plot_platform_comparison(df)

    logger.info("--- Visualization Pipeline Complete ---")
