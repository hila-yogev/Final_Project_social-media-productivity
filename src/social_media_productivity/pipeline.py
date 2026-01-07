### Pipeline file ###

# The pipeline connects the project stages (import -> cleaning -> features -> analysis ...)

from social_media_productivity.config import DATA_PATH
from social_media_productivity.io import load_data


def run_pipeline():
    """
    Stage 1: Data import.
    Loads the full dataset and returns it as a DataFrame.
    """
    # Convert Path to string because pandas accepts both, but this is explicit and clear
    df = load_data(str(DATA_PATH))
    return df
