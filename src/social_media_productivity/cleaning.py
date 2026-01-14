# --------------- Data Processing & Cleaning Module --------------- #

# This module processes and cleans the relevant dataset (all columns).
'''
import pandas as pd

# Import constants 
from src.social_media_productivity.constants import (
    # Numeric/ordinal columns where we impute missing values with the median
    RELEVANT_COLUMNS,
    RELEVANT_COLUMNS_FOR_IMPUTATION,
    IQR_MULTIPLIER,
    # SCORE_COLUMNS_0_10,
    # WINSORIZE_COLUMNS,
)


def calc_medians_and_missing(df: pd.DataFrame) -> tuple[dict, dict]:
    """
    This function calculates medians + count missing values for the target columns (3).

    Returns:
        medians: dict {column_name: median_value}
        missing_counts: dict {column_name: number_of_missing_values}
    """
    # Work on a copy to keep the original data intact
    df_copy = df.copy()

    # Make sure these columns are numeric (non-numeric values become NaN)
    for col in RELEVANT_COLUMNS_FOR_IMPUTATION:
        if col not in df_copy.columns:
            raise ValueError(f"Missing required column: {col}")
        df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")

    # Bonus: count missing values per column
    missing_counts = {col: int(df_copy[col].isna().sum()) for col in TARGET_NUMERIC_COLS}

    # Calculate medians (pandas ignores NaN by default)
    medians = {col: float(df_copy[col].median()) for col in TARGET_NUMERIC_COLS}

    return medians, missing_counts



'''







# --------------- Data Processing & Cleaning Module --------------- #
# This module processes and cleans the relevant dataset one time for analysis.

import pandas as pd
import numpy as np

from src.social_media_productivity.constants import IQR_MULTIPLIER


def clean_and_process_data(df: pd.DataFrame) -> pd.DataFrame:
    """    
    Steps:
    1. Calculate median for the 3 relevant numeric columns
    2. Handle null values by replacing with median (+ count)
    3. Find outliers in daily_social_media_time (+ count)
    4. Apply Winsorization (IQR method) to outliers
    5. Create new productivity_gap column
    """
    
    # Work on a copy to keep the original data intact
    df_clean = df.copy()
    
    # Define the 3 columns we need to handle
    numeric_cols = [
        'actual_productivity_score',
        'perceived_productivity_score', 
        'daily_social_media_time'
    ]
    
    # Convert all numeric columns to float
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    print("=" * 60)
    print("STEP 1-2: NULL VALUES HANDLING")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────
    # STEP 1 & 2: Calculate medians and handle null values
    # ─────────────────────────────────────────────────────────────
    medians = {}
    null_counts = {}
    
    for col in numeric_cols:
        # Calculate median
        median_value = df_clean[col].median()
        medians[col] = median_value
        
        # Count nulls
        null_count = df_clean[col].isna().sum()
        null_counts[col] = null_count
        
        # Replace nulls with median
        df_clean[col].fillna(median_value, inplace=True)
        
        # Print info
        print(f"\n{col}:")
        print(f"   Median: {median_value:.2f}")
        print(f"   Null values: {null_count}")
    
    print("\n" + "=" * 60)
    print("STEP 3-4: OUTLIERS HANDLING (Winsorization)")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────
    # STEP 3 & 4: Find and handle outliers in daily_social_media_time
    # ─────────────────────────────────────────────────────────────
    col = 'daily_social_media_time'
    
    # Calculate Q1, Q3, IQR
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    
    # Calculate upper and lower limits (IQR method)
    lower_limit = q1 - IQR_MULTIPLIER * iqr
    upper_limit = q3 + IQR_MULTIPLIER * iqr
    
    # Count outliers BEFORE winsorization
    # Boolean mask (True/False) identifying outliers in the column
    outliers_mask = (df_clean[col] < lower_limit) | (df_clean[col] > upper_limit)
    outlier_count = outliers_mask.sum()
    
    # Apply winsorization (replace outliers with limits)
    df_clean[col] = df_clean[col].clip(lower=lower_limit, upper=upper_limit)
    
    # Print info
    print(f"\n {col}:")
    print(f"   Q1 (25%): {q1:.2f}")
    print(f"   Q3 (75%): {q3:.2f}")
    print(f"   IQR: {iqr:.2f}")
    print(f"   Lower limit: {lower_limit:.2f}")
    print(f"   Upper limit: {upper_limit:.2f}")
    print(f"   Outliers found: {outlier_count}")
    print(f"   Outliers softened (winsorized)")
    
    print("\n" + "=" * 60)
    print("STEP 5: CREATE PRODUCTIVITY_GAP")
    print("=" * 60)
    
    # ─────────────────────────────────────────────────────────────
    # STEP 5: Create productivity_gap
    # ─────────────────────────────────────────────────────────────
    df_clean['productivity_gap'] = (
        df_clean['perceived_productivity_score'] - 
        df_clean['actual_productivity_score']
    )
    
    print(f"\n✨ New column created: productivity_gap")
    print(f"   Formula: perceived - actual")
    print(f"   Values range: [{df_clean['productivity_gap'].min():.2f}, {df_clean['productivity_gap'].max():.2f}]")
    
    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETE!")
    print("=" * 60)
    print(f"\nDataset shape: {df_clean.shape}")
    print(f"Ready for analysis!\n")
    
    return df_clean







'''



# --------------- Data Processing & Cleaning Module --------------- #
# This module processes and cleans the relevant dataset for analysis.

import pandas as pd
from social_media_productivity.constants import IQR_MULTIPLIER


def clean_and_process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Complete data cleaning and processing pipeline.
    
    Steps (in order):
    1. Handle null values by replacing with median (+ count)
    2. Find and handle outliers in daily_social_media_time with Winsorization (+ count)
    3. Create new productivity_gap column (AFTER data is clean)
    
    Args:
        df: Raw DataFrame from Excel
    
    Returns:
        Cleaned DataFrame with productivity_gap, ready for analysis
    """
    
    # Create a copy to preserve original data
    df_clean = df.copy()
    
    # Define the 3 numeric columns we need to handle
    numeric_cols = [
        'actual_productivity_score',
        'perceived_productivity_score',
        'daily_social_media_time'
    ]
    
    # Convert all numeric columns to float
    for col in numeric_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
    
    print("\n" + "=" * 70)
    print(" STEP 1: NULL VALUES - CALCULATE MEDIAN & REPLACE")
    print("=" * 70)
    
    # ───────────────────────────────────────────────────────────────────
    # STEP 1: Calculate medians and handle null values
    # ───────────────────────────────────────────────────────────────────
    medians = {}
    null_counts = {}
    
    for col in numeric_cols:
        # Calculate median
        median_value = df_clean[col].median()
        medians[col] = median_value
        
        # Count nulls
        null_count = df_clean[col].isna().sum()
        null_counts[col] = null_count
        
        # Replace nulls with median
        df_clean[col].fillna(median_value, inplace=True)
        
        # Print info
        print(f"\n  📊 {col}:")
        print(f"     ✓ Median: {median_value:.2f}")
        print(f"     ✓ Null values replaced: {null_count}")
    
    print("\n" + "=" * 70)
    print(" STEP 2: OUTLIERS - IQR DETECTION & WINSORIZATION")
    print("=" * 70)
    
    # ───────────────────────────────────────────────────────────────────
    # STEP 2: Find outliers and apply Winsorization
    # ───────────────────────────────────────────────────────────────────
    col = 'daily_social_media_time'
    
    # Calculate Q1, Q3, IQR
    q1 = df_clean[col].quantile(0.25)
    q3 = df_clean[col].quantile(0.75)
    iqr = q3 - q1
    
    # Calculate bounds
    lower_limit = q1 - IQR_MULTIPLIER * iqr
    upper_limit = q3 + IQR_MULTIPLIER * iqr
    
    # Count outliers BEFORE winsorization
    outliers_mask = (df_clean[col] < lower_limit) | (df_clean[col] > upper_limit)
    outlier_count = outliers_mask.sum()
    
    # Apply winsorization (replace outliers with limits)
    df_clean[col] = df_clean[col].clip(lower=lower_limit, upper=upper_limit)
    
    # Print info
    print(f"\n  🎯 {col}:")
    print(f"     ✓ Q1 (25th percentile): {q1:.2f}")
    print(f"     ✓ Q3 (75th percentile): {q3:.2f}")
    print(f"     ✓ IQR (Q3 - Q1): {iqr:.2f}")
    print(f"     ✓ Lower limit (Q1 - 1.5*IQR): {lower_limit:.2f}")
    print(f"     ✓ Upper limit (Q3 + 1.5*IQR): {upper_limit:.2f}")
    print(f"     ✓ Outliers detected: {outlier_count}")
    print(f"     ✓ Action: Outliers softened (Winsorization applied)")
    
    print("\n" + "=" * 70)
    print(" STEP 3: CREATE PRODUCTIVITY_GAP (after cleaning)")
    print("=" * 70)
    
    # ───────────────────────────────────────────────────────────────────
    # STEP 3: Create productivity_gap AFTER data is clean
    # Formula: productivity_gap = perceived_productivity_score - actual_productivity_score
    # ───────────────────────────────────────────────────────────────────
    df_clean['productivity_gap'] = (
        df_clean['perceived_productivity_score'] - 
        df_clean['actual_productivity_score']
    )
    
    # Print info
    print(f"\n  ✨ New column created: 'productivity_gap'")
    print(f"     ✓ Formula: perceived - actual")
    print(f"     ✓ Range: [{df_clean['productivity_gap'].min():.2f}, {df_clean['productivity_gap'].max():.2f}]")
    print(f"     ✓ Mean: {df_clean['productivity_gap'].mean():.2f}")
    
    # Final summary
    print("\n" + "=" * 70)
    print(" ✅ DATA CLEANING COMPLETE!")
    print("=" * 70)
    print(f"\n  📈 Final Dataset:")
    print(f"     ✓ Shape: {df_clean.shape} (rows, columns)")
    print(f"     ✓ Null values handled: ✓")
    print(f"     ✓ Outliers softened: ✓")
    print(f"     ✓ productivity_gap created: ✓")
    print(f"\n  🚀 Dataset is ready for analysis!\n")
    
    return df_clean

'''