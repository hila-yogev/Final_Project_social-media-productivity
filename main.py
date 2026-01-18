# --------------- Main Script ---------------
# This is the entry point for the project analysis pipeline.

from src.social_media_productivity.io import load_data
from src.social_media_productivity.cleaning import clean_and_process_data
from src.social_media_productivity.analysis import run_analysis_pipeline
from src.social_media_productivity.visualization import generate_visualizations
from src.social_media_productivity.constants import DATA_PATH, RELEVANT_COLUMNS
from src.social_media_productivity.logger_config import setup_logger

logger = setup_logger()



def main() -> None:
    """
    Main execution function.
    Runs: Load -> Clean -> Analyze -> Visualize.
    """
    logger.info("==========================================")
    logger.info("   STARTING SOCIAL MEDIA ANALYSIS PIPELINE")
    logger.info("==========================================")

    # STAGE 1: Load
    logger.info(">>> STAGE 1: Loading Data")
    df_raw = load_data(DATA_PATH)
    logger.info(f"    Raw data loaded. Rows: {df_raw.shape[0]}, Cols: {df_raw.shape[1]}")

    # STAGE 1.5: Data Overview
    logger.info(">>> STAGE 1.5: Data Overview")
    logger.info("    Displaying only the Relevant Columns for this project:")

    # Select only your 4 specific columns
    try:
        df_overview = df_raw[RELEVANT_COLUMNS]

        # Log the first 5 rows (The Head)
        logger.info("\n" + df_overview.head().to_string())

        # Log the variable types (Int, Float, Object)
        logger.info("\n    Variable Types:\n" + str(df_overview.dtypes))

    except KeyError as e:
        logger.error(f"    Error displaying overview: Missing column {e}")

    # STAGE 2: Clean
    logger.info(">>> STAGE 2: Cleaning Data")
    df_clean = clean_and_process_data(df_raw)
    logger.info(f"    Data cleaning complete. Rows: {df_clean.shape[0]}")

    # STAGE 3: Analyze
    logger.info(">>> STAGE 3: Statistical Analysis")
    run_analysis_pipeline(df_clean)
    logger.info("    Statistical analysis finished. Check logs.")

    # STAGE 4: Visualize
    logger.info(">>> STAGE 4: Visualization")
    generate_visualizations(df_clean)
    logger.info("    Visualizations saved to 'outputs/figures/'.")

    logger.info("==========================================")
    logger.info("   PIPELINE EXECUTION FINISHED SUCCESSFULLY")
    logger.info("==========================================")


if __name__ == "__main__":
    main()