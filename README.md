# Social Media vs Productivity - Final Project (Part II)

**Authors:** Sapir Elihav, Hila Yogev, Shay-El Kalfa

A reproducible Python analysis pipeline that tests whether **daily social media usage**
(time spent) and **preferred social platform** are associated with:
- **Perceived productivity**
- **Actual productivity**
- The **productivity gap** (perceived − actual)

The project is packaged under `src/social_media_productivity/`, uses **logging instead
of print**, includes **unit tests**, and saves **figures and logs** under `outputs/`.

---

## 1) Project Objectives

### Main objectives
1. **Load** a tabular dataset (CSV/XLSX).
2. **Clean & process** core numeric variables (handle invalid values, missingness, outliers).
3. **Generate** a key feature: `productivity_gap`.
4. Run **non-parametric statistical tests** (correlations + group comparisons).
5. Generate and save **visualizations** to support interpretation.
6. Ensure reproducibility via:
   - `requirements.txt`
   - modular design (I/O → cleaning → analysis → visualization)
   - logging
   - tests

### Research question
How are **daily social media time** and **platform preference** related to **perceived
productivity**, **actual productivity**, and the **gap** between them?

### Hypotheses (tested, not assumed true)
- **H1:** Social media time is associated with productivity measures (actual/perceived/gap).
- **H2:** Productivity gap differs across preferred platform groups.

### Assumptions / scope
- Observational dataset → we interpret **associations**, not causation.
- We use **rank-based / non-parametric** tests to reduce sensitivity to non-normality and
ordinal scales.

---

## 2) Data Description + Dataset Link

### Expected local data file
This project expects the dataset at:

- `data/social_media_vs_productivity.xlsx`

The exact expected filename and path are defined in:
- `src/social_media_productivity/constants.py` → `DATA_FILENAME`, `DATA_PATH`

### Dataset source (Kaggle)
- https://www.kaggle.com/datasets/mahdimashayekhi/social-media-vs-productivity

### Core columns used
Defined centrally in `constants.py`:
- `daily_social_media_time`
- `social_platform_preference`
- `perceived_productivity_score`
- `actual_productivity_score`
And an engineered feature:
- `productivity_gap`

---

## 3) Repository Structure

├─ main.py
├─ requirements.txt
├─ data/
│ └─ social_media_vs_productivity.xlsx
├─ outputs/
│ ├─ figures/ # generated plots (PNG)
│ └─ logs/ # pipeline.log
├─ src/
│ └─ social_media_productivity/
│ ├─ constants.py # paths, column names, ALPHA, IQR_MULTIPLIER
│ ├─ logger_config.py # unified logger (console + file)
│ ├─ io.py # load_data() for CSV/XLSX
│ ├─ cleaning.py # imputation + winsorization + gap feature
│ ├─ analysis.py # Spearman, Holm correction, Kruskal-Wallis, robustness checks
│ └─ visualization.py # hist/KDE, scatter+heatmap, platform boxplots
└─ tests/
├─ conftest.py
├─ test_io.py
├─ test_cleaning.py
├─ test_analysis.py
└─ test_visualization.py
---

## 4) Key Pipeline Stages (What happens in each)

The entry point is `main.py`, which runs:

### Stage 1 — Data Import (`io.py`)
- `load_data(DATA_PATH)` loads **CSV** or **Excel** (`.xlsx/.xls`)
- Validates file existence and logs progress.

### Stage 1.5 — Quick Overview (`main.py`)
- Logs the first rows of `RELEVANT_COLUMNS` (if present), for a fast sanity check.

### Stage 2 — Cleaning & Processing (`cleaning.py`)
Cleaning is designed to stabilize analysis without dropping large parts of the dataset:

1) **Type coercion**
   - Converts key numeric columns to numeric with `errors="coerce"` (invalid values become NaN).

2) **Missing value imputation (median)**
   - For numeric analysis columns (`NUMERIC_COLS_FOR_IMPUTATION`), missing values are filled
   with the **median** (robust to outliers).

3) **Outlier handling (Winsorization using IQR)**
   - Applies IQR-based capping (`IQR_MULTIPLIER = 1.5`) to `daily_social_media_time`:
     - lower = Q1 − 1.5×IQR
     - upper = Q3 + 1.5×IQR
   - Uses `clip()` (keeps rows, reduces influence of extremes).

4) **Feature engineering**
   - Creates:
     - `productivity_gap = perceived_productivity_score - actual_productivity_score`

### Stage 3 — Statistical Analysis (`analysis.py`)
The analysis module runs several complementary tests:

1) **Spearman correlations**
   - Computes correlations and logs `(rho, p, n)`.
   - Core “time-family” tests:
     - time vs actual
     - time vs perceived
     - time vs gap
   - Applies **Holm–Bonferroni correction** across these 3 tests before interpreting significance.
   - Additionally reports:
     - actual vs perceived (logged separately, not Holm-corrected as part of the time-family)

2) **Kruskal–Wallis (group differences by platform)**
   - Tests whether `productivity_gap` differs across `social_platform_preference` groups.
   - Logs group sizes and computes effect size **epsilon-squared (ε²)**.
   - If significant (`p < ALPHA`), runs **Dunn post-hoc** (Holm-adjusted) *if scikit-posthocs
     is available*.

3) **Robustness checks**
   - **Time quartile suite:** bins time into quartiles (`pd.qcut`) and runs Kruskal across
     quartiles for actual/perceived/gap (non-linearity check).
   - **Complete-case sensitivity:** reruns key tests using only rows without missing values
     (no imputation) to check if conclusions depend on imputation.

### Stage 4 — Visualization (`visualization.py`)
Figures are saved to `outputs/figures/` (directory created automatically):

1) **Distributions (hist + KDE)** for:
   - time, perceived, actual, gap
   - includes mean/median annotation

2) **Scatter + regression + density heatmap (hexbin)**
   - Combined figure per relationship:
     - actual vs perceived
     - time vs actual
     - time vs perceived
     - time vs gap

3) **Platform comparison boxplots**
   - Separate boxplots by platform for:
     - gap
     - actual
     - perceived

---

## 5) Important Definitions & Key Parameters

### Productivity gap
- `productivity_gap = perceived_productivity_score - actual_productivity_score`

Interpretation:
- **Positive** gap: perceived > actual
- **Negative** gap: perceived < actual

### Key configuration (constants.py)
- `ALPHA = 0.05` (significance threshold)
- `IQR_MULTIPLIER = 1.5` (winsorization threshold)
- `DATA_PATH` / `DATA_FILENAME` (data location)
- Column name constants (prevents “magic strings”)

### Logging behavior (logger_config.py)
- Logs to:
  - console (stdout)
  - `outputs/logs/pipeline.log`
- The log file is overwritten each run (`mode="w"`).
- Prevents duplicate handlers when modules import the logger.

---

## 6) How to Run (Commands)

### Step 1: Clone the repository
```bash
git clone https://github.com/hila-yogev/Final_Project_social-media-productivity.git
cd Final_Project_social-media-productivity
```

### Step 2: Create a virtual environment
```bash
python -m venv .venv
```

### Step 3: Activate the virtual environment

**On Windows:**
```bash
.venv\Scripts\activate
```

**On macOS / Linux:**
```bash
source .venv/bin/activate
```

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the analysis pipeline
```bash
python main.py
```

### Step 6 (Optional): Run tests
```bash
pytest
```