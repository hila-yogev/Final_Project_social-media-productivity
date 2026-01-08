from social_media_productivity.config import DATA_PATH
from social_media_productivity.io import load_data

def test_data_file_exists():
    assert DATA_PATH.exists(), f"Dataset file not found at: {DATA_PATH}"

def test_load_data_returns_dataframe():
    df = load_data(str(DATA_PATH))
    assert df is not None
    assert len(df) > 0
