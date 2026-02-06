# --------------- Analysis Module ---------------
# This module analyzes statistically the dataset.

"""
1) Spearman correlations:
   - time vs actual/perceived/gap (Holm-corrected across 3 tests)
   - actual vs perceived (separated - no Holm)
    
2) Kruskal-Wallis test comparing productivity gap across preferred platforms
   Includes effect size: epsilon-squared.
   If significant, runs Dunn post-hoc test (Holm-adjusted) if available.

3) Complete-case sensitivity analysis (optional, requires df_raw parameter).

Key Design:
- No significance claims before Holm correction
- Results are logged 
- Functions return simple tuples for pipeline stability.
- Enables testing, reporting, and downstream analysis
"""

from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr, kruskal

from src.social_media_productivity.logger_config import setup_logger
from src.social_media_productivity.constants import (
    ALPHA,
    COL_TIME,
    COL_GAP,
    COL_ACTUAL,
    COL_PERCEIVED,
    COL_PLATFORM,
)

logger = setup_logger()


def _holm_adjust(p_values: list[float]) -> list[float]:
    """
    Holm-Bonferroni correction for multiple comparisons.

    Parameters
    ----------
    p_values:
        List of raw p-values (length m).

    Returns
    -------
    list[float]
        Holm-adjusted p-values, in the original order.
    """
    m = len(p_values)
    indexed = list(enumerate(p_values))  # (original_index, p)
    indexed.sort(key=lambda x: x[1])     # sort by p ascending

    adjusted = [0.0] * m
    prev = 0.0

    for rank, (idx, p) in enumerate(indexed):
        # Holm step-down: multiply by remaining hypotheses count
        adj = (m - rank) * p
        # ensure monotonicity (non-decreasing adjusted p-values in sorted order)
        adj = max(adj, prev)
        adj = min(adj, 1.0)

        adjusted[idx] = adj
        prev = adj

    return adjusted


def _run_single_spearman(df: pd.DataFrame, x_col: str, y_col: str) -> tuple[float, float, int]:
    """
    Run Spearman correlation between two columns and log the result.

    Notes
    -----
    - Rows with NaN in either variable are dropped before computing correlation.
    - Spearman is non-parametric and measures monotonic association.
    - No significance determination here (done AFTER Holm correction only).

    Returns
    -------
    (rho, p_value, n)
        rho: Spearman correlation coefficient
        p_value: raw p-value (before Holm correction)
        n: number of valid pairs used in computation
    """
    logger.info(f"Running Spearman Correlation: {x_col} vs {y_col}")

    # Drop rows missing either variable
    pair_df = df[[x_col, y_col]].dropna()
    n = len(pair_df)

    # Guard against constant input (Spearman undefined)
    if pair_df[x_col].nunique() < 2 or pair_df[y_col].nunique() < 2:
        logger.warning(
            f"Spearman undefined for {x_col} vs {y_col}: constant input (n={n})."
        )
        return float("nan"), float("nan"), int(n)

    # Need enough data points for a correlation to be meaningful
    if n < 3:
        logger.warning(
            f"Not enough valid rows for Spearman ({x_col} vs {y_col}). Need >= 3, got {n}."
        )
        return float("nan"), float("nan"), 0

    rho, p_value = spearmanr(pair_df[x_col], pair_df[y_col])
    logger.info(f"   n={n} | rho={rho:.4f}, p-value={p_value:.4f}")

    # Note: No significance claims here. Determination happens AFTER Holm correction.
    # This prevents contradictory messages (raw p says significant, Holm says not).

    return float(rho), float(p_value), int(n)


def run_correlation_suite(df: pd.DataFrame) -> dict[str, tuple[float, float, int]]:
    """
    Run the project's 4 Spearman correlations and apply Holm correction across the relevant ones.

    Tests
    -----
    1) Actual Productivity vs Perceived Productivity
    2) Social Media Time vs Actual Productivity
    3) Social Media Time vs Perceived Productivity
    4) Social Media Time vs Gap

    Returns
    -------
    dict[str, tuple[float, float, int]]
        Mapping from test name to (rho, raw_p_value, n).
        (Holm-adjusted p-values are logged but not returned.)
    """
    logger.info("--- Starting Correlation Suite ---")

    results: dict[str, tuple[float, float, int]] = {}

    # Test 1: Actual vs Perceived
    results["actual_vs_perceived"] = _run_single_spearman(df, COL_ACTUAL, COL_PERCEIVED)
    
    # Test 2-4: Time vs outcomes
    results["actual"] = _run_single_spearman(df, COL_TIME, COL_ACTUAL)
    results["perceived"] = _run_single_spearman(df, COL_TIME, COL_PERCEIVED)
    results["gap"] = _run_single_spearman(df, COL_TIME, COL_GAP)

    # ---- Multiple comparisons correction (Holm) ONLY for time-based tests ----
    # actual_vs_perceived is reported separately (not part of the time-family)

    p_actual_vs_perceived = results["actual_vs_perceived"][1]

    time_tests = ["actual", "perceived", "gap"]  # the 3 primary hypothesis tests
    time_raw_pvals = [results[name][1] for name in time_tests]

    # If any p-values are nan, Holm is not meaningful -> skip correction
    if pd.isna(p_actual_vs_perceived) or any(pd.isna(p) for p in time_raw_pvals):
        logger.warning("Holm correction skipped because at least one p-value is NaN.")
        logger.info(
            f"actual_vs_perceived (separate): rho={results['actual_vs_perceived'][0]:.4f} | "
            f"p(raw, not corrected)={p_actual_vs_perceived:.4f}"
        )
        return results

    time_adjusted = _holm_adjust(time_raw_pvals)

    # Logging
    logger.info("--- Spearman p-values ---")
    logger.info(
        f"actual_vs_perceived (separate, no Holm): n={results['actual_vs_perceived'][2]} | "
        f"rho={results['actual_vs_perceived'][0]:.4f} | p_raw={p_actual_vs_perceived:.4f}"
)

    logger.info("--- Holm correction applied to the 3 time-based tests only ---")
    for name, raw_p, holm_p in zip(time_tests, time_raw_pvals, time_adjusted):
        logger.info(
            f"time vs {name}: rho={results[name][0]:.4f} | "
            f"p(raw, not corrected)={raw_p:.4f} | p(Holm corrected)={holm_p:.4f}"
        )


    return results

def run_kruskal_wallis(df: pd.DataFrame) -> tuple[float, float]:
    """
    Run Kruskal-Wallis test: Does productivity gap differ across platform groups?

    Adds:
    - group sizes
    - effect size: epsilon-squared (ε²)

    If significant (p < ALPHA), runs Dunn post-hoc test (Holm-adjusted) if available.

    Returns
    -------
    (h_stat, p_value)
    """
    logger.info(f"Running Kruskal-Wallis Test: {COL_GAP} by {COL_PLATFORM}")

    kw_df = df[[COL_PLATFORM, COL_GAP]].dropna()
    n_total = len(kw_df)

    platforms = kw_df[COL_PLATFORM].unique()

    groups: list[pd.Series] = []
    kept_platforms: list[str] = []

    for p in platforms:
        g = kw_df.loc[kw_df[COL_PLATFORM] == p, COL_GAP]
        if len(g) > 0:
            kept_platforms.append(p)
            groups.append(g)

    k = len(groups)

    if k < 2:
        logger.warning("Not enough non-empty platform groups for Kruskal-Wallis.")
        return float("nan"), float("nan")

    # Log group sizes (for the groups actually tested)
    logger.info("--- Platform group sizes (n) ---")
    for p in kept_platforms:
        size = int((kw_df[COL_PLATFORM] == p).sum())
        logger.info(f"   {p}: n={size}")

    h_stat, p_value = kruskal(*groups)
    logger.info(
        f"Kruskal-Wallis Result: H-stat={h_stat:.4f}, p-value={p_value:.4f} | N={n_total}, k={k}"
    )

    # Effect size (epsilon-squared) for Kruskal-Wallis:
    # ε² = (H - k + 1) / (N - k)
    if n_total > k:
        eps_sq = max(0.0, (h_stat - k + 1) / (n_total - k))
        logger.info(f"Effect size (epsilon-squared, ε²) = {eps_sq:.4f}")
        if eps_sq < 0.01:
            size_label = "negligible (very small effect)"
        elif eps_sq < 0.06:
            size_label = "small effect"
        elif eps_sq < 0.14:
            size_label = "medium effect"
        else:
            size_label = "large effect"

        logger.info(f"Meaning: ε² indicates a {size_label}.")

    else:
        logger.warning("Could not compute epsilon-squared (N <= k).")

    if p_value < ALPHA:
        logger.info(">> Significant differences found between platforms.")
        _run_dunn_posthoc_if_available(kw_df)
    else:
        logger.info(">> No significant difference found between platforms.")

    return float(h_stat), float(p_value)


def _run_dunn_posthoc_if_available(kw_df: pd.DataFrame) -> None:
    """
    If scikit-posthocs is installed, run Dunn's post-hoc test after significant Kruskal.

    Dunn test performs pairwise comparisons between groups and returns a p-value matrix.
    We apply Holm correction to control familywise error across comparisons.
    """
    try:
        import scikit_posthocs as sp  # dependency already listed in requirements.txt

        logger.info("--- Running Dunn post-hoc test (Holm-adjusted) ---")
        p_matrix = sp.posthoc_dunn(
            kw_df,
            val_col=COL_GAP,
            group_col=COL_PLATFORM,
            p_adjust="holm",
        )

        # Log as a table (matrix of adjusted p-values)
        logger.info("Dunn post-hoc p-values (Holm-adjusted):")
        logger.info("\n" + p_matrix.to_string())

    except ImportError:
        logger.warning("scikit-posthocs not available -> skipping Dunn post-hoc.")

    except Exception as e:
        logger.warning(f"Dunn post-hoc failed: {e}")


def run_time_quartile_suite(df: pd.DataFrame) -> None:
    """
    Check for non-linear relationships by binning social media time into quartiles
    and comparing outcomes across bins using Kruskal-Wallis.

    Tests:
    - actual productivity across quartiles
    - perceived productivity across quartiles
    - productivity gap across quartiles
    """
    logger.info("--- Starting Time Quartile Suite (non-linearity check) ---")

    # We need time + outcomes, drop missing
    cols_needed = [COL_TIME, COL_ACTUAL, COL_PERCEIVED, COL_GAP]
    q_df = df[cols_needed].dropna()

    if len(q_df) < 10:
        logger.warning("Not enough rows for quartile analysis.")
        return

    # Quantile-binning time into ~4 equal groups - "quartiles" 
    # More robust: if qcut drops bins, labels will still match -  duplicates='drop' protects against constant values edge case.
    # so we use labels=False (auto bin codes) +1 for readable 1..k labels and to avoid label/bins mismatch errors.
    q_df["time_quartile"] = pd.qcut(q_df[COL_TIME], q=4, labels=False, duplicates="drop") + 1

    # If qcut had to drop bins (rare), ensure we still have >=2 groups
    quartiles = sorted(q_df["time_quartile"].dropna().astype(int).unique())
    if len(quartiles) < 2:
        logger.warning("Quartile binning produced <2 groups; skipping quartile suite.")
        return
    
    # Log how many groups were created
    n_groups = q_df["time_quartile"].nunique()
    logger.info(f"Time quartile binning created {n_groups} groups (1..{n_groups}).")

    # Log medians by quartile (very interpretable)
    logger.info("Medians by time quartile:")
    med_table = (
        q_df.groupby("time_quartile", observed=False)[[COL_ACTUAL, COL_PERCEIVED, COL_GAP]]
        .median()
    )
    logger.info("\n" + med_table.to_string())

    # Helper to run Kruskal across quartiles for a single outcome
    def _kw_by_quartile(outcome_col: str) -> None:
        groups = [q_df.loc[q_df["time_quartile"] == q, outcome_col] for q in sorted(quartiles)]
        h, p = kruskal(*groups)
        logger.info(f"Kruskal across time quartiles for {outcome_col}: H={h:.4f}, p={p:.4f}")

    _kw_by_quartile(COL_ACTUAL)
    _kw_by_quartile(COL_PERCEIVED)
    _kw_by_quartile(COL_GAP)

    logger.info("--- Time Quartile Suite Complete ---")


def run_complete_case_sensitivity(df_raw: pd.DataFrame) -> None:
    """
    Sensitivity analysis: rerun the core tests using complete-case data (no imputation).
    checks whether conclusions depend on the imputation strategy.
    """
    logger.info("--- Starting Complete-Case Sensitivity Analysis ---")

    # Use only rows with no missing values in core columns
    needed = [COL_TIME, COL_PLATFORM, COL_PERCEIVED, COL_ACTUAL]
    cc = df_raw[needed].dropna()

    # Create gap on complete-case subset
    cc = cc.copy()
    cc[COL_GAP] = cc[COL_PERCEIVED] - cc[COL_ACTUAL]

    logger.info(f"Complete-case n={len(cc)} (out of {len(df_raw)})")

    # Rerun key tests on complete-case
    run_correlation_suite(cc)
    run_kruskal_wallis(cc)          # platform differences in gap
    run_time_quartile_suite(cc)     # non-linearity check

    logger.info("--- Complete-Case Sensitivity Analysis Complete ---")


def run_analysis_pipeline(df: pd.DataFrame, df_raw: pd.DataFrame | None = None) -> None:
    """Orchestrator function: runs all statistical tests in the correct order."""
    logger.info("--- Starting Statistical Analysis ---")

    run_correlation_suite(df)
    run_kruskal_wallis(df)
    run_time_quartile_suite(df)

    if df_raw is not None:
        run_complete_case_sensitivity(df_raw)

    logger.info("--- Statistical Analysis Complete ---")
