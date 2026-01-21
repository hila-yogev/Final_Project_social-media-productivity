"""
constants.py

Central place for project constants:
- Paths
- Column names (avoid "magic strings" scattered across files)
- Statistical configuration (alpha)
- Cleaning configuration (IQR multiplier, etc.)
"""

from pathlib import Path

# ---------- Project paths ----------
# Project root is the folder that contains: data/, outputs/, src/, main.py
PROJECT_ROOT: Path = Path(__file__).resolve().parents[2]

DATA_DIR: Path = PROJECT_ROOT / "data"
OUTPUTS_DIR: Path = PROJECT_ROOT / "outputs"
FIGURES_DIR: Path = OUTPUTS_DIR / "figures"
LOGS_DIR: Path = OUTPUTS_DIR / "logs"

# IMPORTANT: must match the actual file name inside /data
DATA_FILENAME: str = "social_media_vs_productivity.xlsx"
DATA_PATH: Path = DATA_DIR / DATA_FILENAME

# ---------- Column names ----------
COL_TIME: str = "daily_social_media_time"
COL_PLATFORM: str = "social_platform_preference"
COL_PERCEIVED: str = "perceived_productivity_score"
COL_ACTUAL: str = "actual_productivity_score"
COL_GAP: str = "productivity_gap"

# Columns needed for this project’s core pipeline
RELEVANT_COLUMNS: list[str] = [COL_TIME, COL_PLATFORM, COL_PERCEIVED, COL_ACTUAL]

# Numeric columns where missing values will be imputed with the median
NUMERIC_COLS_FOR_IMPUTATION: list[str] = [COL_TIME, COL_PERCEIVED, COL_ACTUAL]

# ---------- Statistical configuration ----------
ALPHA: float = 0.05

# ---------- Cleaning configuration ----------
IQR_MULTIPLIER: float = 1.5
