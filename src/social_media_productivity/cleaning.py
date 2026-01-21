# --------------- Data Processing & Cleaning Module ---------------
# This module processes and cleans the dataset.

# Import pandas for data manipulation
import pandas as pd

# Import project constants
from src.social_media_productivity.constants import (
    IQR_MULTIPLIER,
    NUMERIC_COLS_FOR_IMPUTATION,
    COL_TIME,
    COL_GAP,
    COL_PERCEIVED,
    COL_ACTUAL,
)


# Import our custom logger
from src.social_media_productivity.logger_config import setup_logger

# Initialize the logger
logger = setup_logger()


def _impute_missing_values(df: pd.DataFrame, cols: list[str]) -> None:
    """Helper: Replaces missing values with the median."""
    for col in cols:
        median_val = df[col].median()
        missing_count = df[col].isna().sum()
        df[col] = df[col].fillna(median_val)

        if missing_count > 0:
            logger.info(f"Imputed {missing_count} missing values in '{col}' with median: {median_val:.2f}")


def _winsorize_column(df: pd.DataFrame, col: str) -> None:
    """Helper: Caps outliers using the IQR method (Winsorization)."""
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    lower_limit = q1 - (iqr * IQR_MULTIPLIER)
    upper_limit = q3 + (iqr * IQR_MULTIPLIER)

    before = df[col].copy()
    df[col] = df[col].clip(lower=lower_limit, upper=upper_limit)

    changed_count = (before != df[col]).sum()
    logger.info(
        f"Winsorized '{col}'. Limits: [{lower_limit:.2f}, {upper_limit:.2f}]. "
        f"Capped values: {changed_count}"
    )



def clean_and_process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Orchestrates the data cleaning pipeline.
    """
    df_clean = df.copy()

    # Ensure relevant columns are numeric
    for col in NUMERIC_COLS_FOR_IMPUTATION:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

    # Step 1: Handle missing values
    _impute_missing_values(df_clean, NUMERIC_COLS_FOR_IMPUTATION)

    # Step 2: Handle outliers
    _winsorize_column(df_clean, COL_TIME)

    # Step 3: Create 'productivity_gap' (Perceived - Actual)
    df_clean[COL_GAP] = df_clean[COL_PERCEIVED] - df_clean[COL_ACTUAL]

    logger.info("Created new feature: 'productivity_gap'")

    return df_clean