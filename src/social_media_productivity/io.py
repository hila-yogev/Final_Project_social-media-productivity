# --------------- IO Module ---------------

# This module handles data loading.

# --- Libraries ---
# Import all useful libraries
import pandas as pd
from pathlib import Path

# --- Functions ---
def load_data(file_path: str) -> pd.DataFrame:
    # Load the dataset from a CSV/XLSX file into a pandas DataFrame.
    file_path = Path(file_path)  # converts str to Path if needed

    try:
        # Load CSV
        if file_path.suffix.lower() == ".csv":
            return pd.read_csv(file_path)

        # Load Excel (XLSX / XLS)
        if file_path.suffix.lower() in {".xlsx", ".xls"}:
            return pd.read_excel(file_path)

        # Unsupported file type
        raise ValueError("Unsupported file type - use XLSX, XLS or CSV.")

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except Exception as e:
        raise RuntimeError(f"Failed to load the dataset. Details: {e}")
