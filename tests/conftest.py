"""
conftest.py

pytest fixtures shared across tests.

Why fixtures:
- Avoid repeating expensive I/O (loading Excel) in every test
- Provide consistent test inputs for cleaning/analysis/visualization
"""

import pandas as pd
import pytest

from src.social_media_productivity.constants import DATA_PATH
from src.social_media_productivity.io import load_data
from src.social_media_productivity.cleaning import clean_and_process_data


@pytest.fixture(scope="session")
def df_raw() -> pd.DataFrame:
    """Raw dataset loaded from the project data/ folder."""
    return load_data(DATA_PATH)


@pytest.fixture(scope="session")
def df_clean(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Cleaned dataset produced by the project's cleaning pipeline."""
    return clean_and_process_data(df_raw)
