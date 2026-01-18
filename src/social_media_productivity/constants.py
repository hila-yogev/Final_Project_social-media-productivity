# --------------- Constants Module ---------------
# This module stores project-wide constants to avoid magic numbers.

# Import Path for robust file system path handling
from pathlib import Path

DATA_PATH = Path("data/social_media_vs_productivity.xlsx")
#DATA_PATH = Path(r'C:\Users\shayel\Desktop\pycharm projects\Final_Project_social-media-productivity\data\social_media_vs_productivity.xlsx')
# List of columns relevant to our specific research question
RELEVANT_COLUMNS = [
    "daily_social_media_time",
    "social_platform_preference",
    "perceived_productivity_score",
    "actual_productivity_score",
]

# List of numeric columns where missing values will be replaced by the median
RELEVANT_COLUMNS_FOR_IMPUTATION = [
    "daily_social_media_time",
    "perceived_productivity_score",
    "actual_productivity_score",
]

# The multiplier for the Interquartile Range (IQR) method (standard is 1.5)
IQR_MULTIPLIER = 1.5