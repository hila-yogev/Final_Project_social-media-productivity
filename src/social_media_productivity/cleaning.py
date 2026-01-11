# --- Cleaning stage ---
# This module is responsible for data cleaning and preprocessing.

import pandas as pd


SCORE_COLUMNS_0_10 = [
    "perceived_productivity_score",
    "actual_productivity_score",
    "stress_level",
    "job_satisfaction_score",
]


def _set_out_of_range_scores_to_nan(df: pd.DataFrame) -> pd.DataFrame:
    """
    Replace out-of-range values (outside 0-10) with NaN for score columns.
    This enforces the project's basic assumptions.
    """
    df = df.copy()

    for col in SCORE_COLUMNS_0_10:
        if col in df.columns:
            df.loc[(df[col] < 0) | (df[col] > 10), col] = pd.NA

    return df


def _median_impute(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Fill missing values using the median (robust to outliers).
    """
    df = df.copy()

    for col in columns:
        if col in df.columns:
            median_value = df[col].median(skipna=True)
            df[col] = df[col].fillna(median_value)

    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main cleaning function (major stage).
    Current steps:
    1) Enforce valid ranges for score columns (0-10).
    2) Impute missing values (median) for key analysis columns.
    """
    df_clean = df.copy()

    # Step 1: enforce valid score ranges
    df_clean = _set_out_of_range_scores_to_nan(df_clean)

    # Step 2: impute missing values for core columns used in analysis
    key_cols_for_imputation = [
        "daily_social_media_time",
        "perceived_productivity_score",
        "actual_productivity_score",
    ]
    df_clean = _median_impute(df_clean, key_cols_for_imputation)

    return df_clean
