"""
test_io.py

Tests for io.py:
- loads the dataset successfully from DATA_PATH
- raises FileNotFoundError for missing files
"""

from pathlib import Path

import pandas as pd
import pytest

from src.social_media_productivity.io import load_data
from src.social_media_productivity.constants import DATA_PATH


def test_load_data_success() -> None:
    """Dataset file exists and is loadable into a DataFrame."""
    df = load_data(DATA_PATH)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] > 0, "Expected at least 1 row in the dataset."


def test_load_data_missing_file_raises() -> None:
    """Loading a non-existent file should raise FileNotFoundError."""
    fake_path = Path("data/this_file_does_not_exist.xlsx")
    with pytest.raises(FileNotFoundError):
        load_data(fake_path)
