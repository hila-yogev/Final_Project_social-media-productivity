### input output file ###


# --- Libraries ---
# Import all useful libraries
import pandas as pd


# --- Functions ---

def load_data(file_path: str) -> pd.DataFrame:
    # Load the dataset from a CSV/XLSX file into a pandas DataFrame.

    try:
        # Load CSV
        if file_path.lower().endswith(".csv"):
            return pd.read_csv(file_path)

        # Load Excel (XLSX / XLS)
        if file_path.lower().endswith((".xlsx", ".xls")):
            return pd.read_excel(file_path)

        # Unsupported file type
        raise ValueError("Unsupported file type - use XLSX, XLS or CSV.")

    except FileNotFoundError:
        # File does not exist at the given path
        raise FileNotFoundError(f"File not found: {file_path}")

    except Exception as e:
        # Any other issue (permissions, parsing, etc.)
        raise RuntimeError(f"Failed to load the dataset. Details: {e}")
