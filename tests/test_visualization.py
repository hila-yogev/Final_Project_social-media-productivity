"""
test_visualization.py

Tests for visualization.py:
- running generate_visualizations creates expected PNG files in outputs/figures
"""

from pathlib import Path
import pandas as pd

from src.social_media_productivity.visualization import generate_visualizations
from src.social_media_productivity.constants import (
    FIGURES_DIR,
    COL_TIME,
    COL_PERCEIVED,
    COL_ACTUAL,
    COL_GAP,
    COL_PLATFORM,
)


def test_generate_visualizations_creates_files(df_clean: pd.DataFrame) -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    expected_files = [
        # distributions
        f"distribution_{COL_TIME}.png",
        f"distribution_{COL_PERCEIVED}.png",
        f"distribution_{COL_ACTUAL}.png",
        f"distribution_{COL_GAP}.png",
        # scatter and heatmap suite
        f"scatter_and_heatmap_{COL_ACTUAL}_vs_{COL_PERCEIVED}.png",
        f"scatter_and_heatmap_{COL_TIME}_vs_{COL_ACTUAL}.png",
        f"scatter_and_heatmap_{COL_TIME}_vs_{COL_PERCEIVED}.png",
        f"scatter_and_heatmap_{COL_TIME}_vs_{COL_GAP}.png",
        # platform boxplots
        "platform_boxplot_gap.png",
        "platform_boxplot_actual.png",
        "platform_boxplot_perceived.png",
    ]

    # Clean previous outputs for a deterministic test
    for fname in expected_files:
        fpath = FIGURES_DIR / fname
        if fpath.exists():
            fpath.unlink()

    # Run the visualization pipeline
    generate_visualizations(df_clean)

    # Assert all figures were created and are non-empty
    for fname in expected_files:
        fpath = FIGURES_DIR / fname
        assert fpath.exists(), f"Expected figure file not found: {fpath}"
        assert fpath.stat().st_size > 0, f"Figure file is empty: {fpath}"
