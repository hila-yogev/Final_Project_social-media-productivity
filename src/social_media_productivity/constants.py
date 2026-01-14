# --------------- Constants Module ---------------
# Keep important paths and constants in one place.

from pathlib import Path

# Path to the dataset (XLSX)
DATA_PATH = Path("data/social_media_vs_productivity.xlsx")

# Columns used in our research question
RELEVANT_COLUMNS = [
    "daily_social_media_time",
    "social_platform_preference",
    "perceived_productivity_score",
    "actual_productivity_score",
]

# Numeric/ordinal columns where we impute missing values with the median
RELEVANT_COLUMNS_FOR_IMPUTATION = [
    "daily_social_media_time",
    "perceived_productivity_score",
    "actual_productivity_score",
]

# IQR rule configuration for winsorization
IQR_MULTIPLIER = 1.5
