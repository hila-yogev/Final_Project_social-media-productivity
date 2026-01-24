# Social Media vs Productivity - Final Project (Part II)

**Authors:** Sapir Elihav, Hila Yogev, Shay-El Kalfa

## Project Overview
This project analyzes the relationship between **daily social media usage** and productivity outcomes:

- `perceived_productivity_score`
- `actual_productivity_score`
- `productivity_gap = perceived_productivity_score - actual_productivity_score`

### Research goals
1. Test whether more time on social media is associated with productivity outcomes.
2. Test whether the **productivity gap** differs across preferred social platforms.

### Hypotheses
- **H1:** Higher `daily_social_media_time` is associated with lower `actual_productivity_score`.
- **H2:** Higher `daily_social_media_time` is associated with a larger `productivity_gap`.
- **H3:** `productivity_gap` differs across `social_platform_preference` groups.

---

## Dataset
**Source:** Kaggle — *Social*


additions:

This project applies targeted data cleaning only to variables
directly involved in the research question, in order to avoid
unnecessary assumptions on unrelated features.

Note on Missing Value Imputation

Missing values in key variables were handled using median imputation to preserve sample size and robustness to outliers. This approach may introduce repeated values at the median, which can appear as horizontal or vertical bands in some visualizations. These patterns reflect preprocessing effects rather than meaningful behavioral structures and are taken into account when interpreting results.