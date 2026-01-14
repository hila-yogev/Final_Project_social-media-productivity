# --------------- Main Script ---------------
# Each function call represents a major stage.
"""
from social_media_productivity.io import load_data
from social_media_productivity.cleaning import clean_and_process_data
from social_media_productivity.constants import DATA_PATH

def main() -> None:
    # Stage 1: Data import
    df = load_data(DATA_PATH)

    # Quick sanity check (temporary)
    print("Dataset loaded successfully!")
    print("Shape:", df.shape)
  
    print(df.head())

    # Stage 2: Data cleaning (will be added)
    # df = clean_data(df)

    # Stage 3: Feature engineering (will be added)
    # df = add_features(df)

    # Stage 4: Statistical tests (will be added)
    # stats_results = run_stat_tests(df)

    # Stage 5: Modeling (will be added)
    # model_results = run_models(df)

    # Stage 6: Visualizations / outputs (will be added)
    # save_outputs(df, stats_results, model_results)

if __name__ == "__main__":
    main()

"""

"""

# --- Main Script ---
# Each function call represents a major stage.
from src.social_media_productivity.io import load_data
from src.social_media_productivity.cleaning import clean_and_process_data
from src.social_media_productivity.constants import DATA_PATH

def main() -> None:
 
    # Stage 1: Load data
    print("\n" + "=" * 70)
    print(" STAGE 1: LOADING DATA")
    print("=" * 70)
    df = load_data(DATA_PATH)
    
    # Stage 2: Clean data
    print("\n" + "=" * 70)
    print(" STAGE 2: CLEANING & PROCESSING DATA")
    print("=" * 70)
    df_clean = clean_and_process_data(df)
    
    # Pipeline complete
    print("\n" + "=" * 70)
    print(" ✅ PIPELINE COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()

"""

    # --- Main Script ---
# Each function call represents a major stage.
from src.social_media_productivity.io import load_data
from src.social_media_productivity.cleaning import clean_and_process_data
from src.social_media_productivity.constants import DATA_PATH

def main() -> None:
    
    # Stage 1: Load data
    print("\n" + "=" * 70)
    print(" STAGE 1: LOADING DATA")
    print("=" * 70)
    df = load_data(DATA_PATH)
    print(f"\n✓ Raw data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"  Columns: {df.columns.tolist()}")
    
    # Stage 2: Clean data
    print("\n" + "=" * 70)
    print(" STAGE 2: CLEANING & PROCESSING DATA")
    print("=" * 70)
    df_clean = clean_and_process_data(df)
    
    # Stage 3: Summary report
    print("\n" + "=" * 70)
    print(" STAGE 3: CLEANING SUMMARY")
    print("=" * 70)
    
    print(f"\n📊 Final Dataset Information:")
    print(f"  Shape: {df_clean.shape[0]} rows × {df_clean.shape[1]} columns")
    
    print(f"\n📋 Columns in cleaned dataset:")
    for i, col in enumerate(df_clean.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\n🔍 Missing values in cleaned data:")
    missing_info = df_clean.isnull().sum()
    if missing_info.sum() == 0:
        print(f"  ✓ All missing values have been imputed!")
    else:
        for col, count in missing_info.items():
            if count > 0:
                print(f"  - {col}: {count} missing values")
    
    # Pipeline complete
    print("\n" + "=" * 70)
    print(" ✅ MAIN COMPLETE")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main() 