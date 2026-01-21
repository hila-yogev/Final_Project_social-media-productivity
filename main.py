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
    Runs: Load -> Display -> Clean -> Analyze -> Visualize.
    """
    logger.info("==========================================")
    logger.info("   STARTING SOCIAL MEDIA ANALYSIS PIPELINE")
    logger.info("==========================================")

    # STAGE 1: Load
    logger.info(">>> STAGE 1: Loading Data")
    df_raw = load_data(DATA_PATH)
    logger.info(f"    Raw data loaded. Rows: {df_raw.shape[0]}, Cols: {df_raw.shape[1]}")

    # STAGE 1.5: Overview
    logger.info(">>> STAGE 1.5: Data Overview")
    try:
        df_overview = df_raw[RELEVANT_COLUMNS]
        logger.info("\n" + df_overview.head().to_string())
    except KeyError:
        logger.warning("    Some relevant columns missing in raw data (will be handled in cleaning).")

    # STAGE 2: Clean
    logger.info(">>> STAGE 2: Cleaning Data")
    df_clean = clean_and_process_data(df_raw)

    # STAGE 3: Analyze
    logger.info(">>> STAGE 3: Statistical Analysis")
    run_analysis_pipeline(df_clean)

    # STAGE 4: Visualize
    logger.info(">>> STAGE 4: Visualization")
    generate_visualizations(df_clean)
    logger.info("    Visualizations saved to 'outputs/figures/'.")

    logger.info("==========================================")
    logger.info("   PIPELINE EXECUTION FINISHED SUCCESSFULLY")
    logger.info("==========================================")


if __name__ == "__main__":
    main()