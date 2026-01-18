# --------------- IO Module ---------------
# This module handles data loading from files.

# Import pandas for DataFrame handling
import pandas as pd

# Import Path for robust file path handling
from pathlib import Path

# Import our custom logger setup
from src.social_media_productivity.logger_config import setup_logger

# Initialize the logger for this module
logger = setup_logger()


def load_data(file_path: Path) -> pd.DataFrame:
    """
    Loads the dataset from a CSV or Excel file.
    """
    # PROJECT_ROOT = Path(__file__).resolve().parent[2]
    # print(f"PROJECT_ROOT: {PROJECT_ROOT}")

    # Log the attempt to start loading data
    logger.info(f"Attempting to load data from: {file_path}")

    # Ensure the file actually exists
    if not file_path.exists():
        logger.error(f"File not found at: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Check if the file is a CSV
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)
            logger.info("Successfully loaded CSV file.")
            return df

        # Check if the file is an Excel file
        elif file_path.suffix.lower() in {".xlsx", ".xls"}:
            df = pd.read_excel(file_path)
            logger.info("Successfully loaded Excel file.")
            return df

        # If file extension is not recognized
        else:
            raise ValueError("Unsupported file type. Use .csv or .xlsx")

    except Exception as e:
        logger.error(f"Failed to load data. Error: {e}")
        raise