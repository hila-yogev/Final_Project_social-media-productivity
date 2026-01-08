# --- Main Script ---
# This file stays minimal and calls key functions (major stages).

from social_media_productivity.config import DATA_PATH
from social_media_productivity.io import load_data


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
