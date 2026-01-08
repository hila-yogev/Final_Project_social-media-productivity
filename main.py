# --- Main script ---
# This file should stay minimal: it only runs the pipeline.

from social_media_productivity.pipeline import run_pipeline


def main():
    # Run the pipeline and print a quick confirmation
    df = run_pipeline()
    print("Dataset loaded successfully!")
    print("Shape:", df.shape)
    print(df.head())


if __name__ == "__main__":
    main()
