"""
test_analysis.py

Tests for analysis.py:
- correlation suite returns all keys and numeric outputs
- kruskal returns numeric outputs
"""

import math
import pandas as pd

from src.social_media_productivity.analysis import run_correlation_suite, run_kruskal_wallis


def _is_number(x: float) -> bool:
    """True if x is a float/int including NaN (we accept NaN as a valid float result)."""
    return isinstance(x, (int, float))


def test_run_correlation_suite_returns_expected_keys(df_clean: pd.DataFrame) -> None:
    results = run_correlation_suite(df_clean)

    assert isinstance(results, dict)
    assert set(results.keys()) == {"gap", "actual", "perceived", "actual_vs_perceived"}

    for key, (rho, p, n) in results.items():
        assert _is_number(rho), f"{key}: rho should be numeric"
        assert _is_number(p), f"{key}: p-value should be numeric"
        assert _is_number(n), f"{key}: n should be numeric"

def test_run_kruskal_wallis_returns_numbers(df_clean: pd.DataFrame) -> None:
    h_stat, p_value = run_kruskal_wallis(df_clean)

    assert _is_number(h_stat)
    assert _is_number(p_value)
