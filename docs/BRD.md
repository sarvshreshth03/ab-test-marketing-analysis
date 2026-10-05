# Business Requirements Document
**Project:** Marketing A/B Test Analysis — Ad vs. PSA Conversion Lift
**Status:** Completed (Day 1)

## Business Question
Did displaying marketing advertisements causally increase conversion rates compared to the Public Service Announcement (PSA) control, and is the effect large enough to justify scaling ads to 100% of user traffic going forward?

## Hypotheses
- **$H_0$ (Null Hypothesis):** $p_{\text{ad}} - p_{\text{psa}} = 0$ (The ad campaign has no causal effect on conversion rate compared to the PSA control).
- **$H_1$ (Alternative Hypothesis):** $p_{\text{ad}} - p_{\text{psa}} \neq 0$ (The ad campaign causes a statistically significant difference in conversion rate).

## Primary Metric
- **Conversion Rate (CR):** The proportion of exposed users who converted (`converted == True` / total unique users per variant).

## Guardrail Metrics
- **Sample Ratio Mismatch (SRM):** Ensure traffic distribution strictly mirrors expected assignment ratios (nominal 96:4 split).
- **Segment Consistency:** Ensure lift is directionally positive across interaction hours and days (absence of Simpson's paradox).

## Minimum Detectable Effect (MDE) and Power Sensitivity
- **Baseline Conversion Rate ($p_{\text{control}}$):** 1.785% (420 conversions / 23,524 control users).
- **Target MDE:** 10% relative lift ($p_{\text{treatment}} \ge 1.964\%$).
- **Significance ($\alpha$):** 0.05 (two-sided).
- **Power ($1 - \beta$):** 0.80.
- **Power Reality:** Due to severe traffic imbalance (ratio $\approx 24.0$), detecting a subtle 10% lift required ~47,155 PSA control users. With 23,524 users, the experiment was underpowered for a 10% lift, though adequately sensitive to detect larger swings ($\ge 15\%$).
