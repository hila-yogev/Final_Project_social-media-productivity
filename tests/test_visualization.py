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
        # detailed time histogram
        "social_media_time_detailed.png",
        # scatter suite (named by y variable in your code)
        f"scatter_{COL_GAP}.png",
        f"scatter_{COL_ACTUAL}.png",
        f"scatter_{COL_PERCEIVED}.png",
        # platform boxplot
        "platform_boxplot.png",
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
