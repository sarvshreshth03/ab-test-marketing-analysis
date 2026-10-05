# Executive Insights Memo: Marketing A/B Test Analysis (Ad vs. PSA)

**To:** Marketing Leadership & Growth Engineering  
**From:** Data Analytics & Experimentation Team  
**Date:** October 5, 2026  
**Subject:** Ad Exposure Impact on User Conversion Lift  

---

## 1. Executive Summary

We evaluated experiment data from 588,101 users to measure whether ad exposure causally lifts user conversion rates over a Public Service Announcement (PSA) control[cite: 2]. 

**Recommendation: Roll out the ad experience to 100% of traffic[cite: 2].**  
Exposing users to ads generated a statistically significant relative lift in conversion of **+43.09% (95% CI: [+33.33%, +52.84%], $p = 1.71 \times 10^{-13}$)**[cite: 2]. The observed effect size exceeds the initial 10% Minimum Detectable Effect (MDE)[cite: 2]. Subgroup analysis across exposure days shows uniform positive lift with no Simpson's paradox reversals[cite: 2].

---

## 2. Key Experimental Metrics

| Metric | Ad Variant (Treatment) | PSA (Control) | Difference / Lift | Statistical Significance |
|---|---|---|---|---|
| **User Count** | 564,577 (96.00%) | 23,524 (4.00%) | Allocation Ratio: 24.0:1 | SRM $p = 0.9998$ (Clean)[cite: 2] |
| **Conversions** | 14,423 | 420 | +14,003 conversions | — |
| **Conversion Rate** | **2.5547%** | **1.7854%** | **+0.7692 pp** (Absolute) | $z = 7.3701$[cite: 2] |
| **Relative Lift** | — | — | **+43.09%** | $p = 1.705 \times 10^{-13}$[cite: 2] |
| **95% Confidence Interval**| [2.51%, 2.60%] | [1.62%, 1.95%] | **[+33.33%, +52.84%]** | Excludes 0 (Statistically Significant)[cite: 2] |

* **Power Sensitivity:** Due to the 96:4 imbalance, detecting an MDE of 10% required 47,155 control users[cite: 2]. Although the control group had 23,524 users (making it underpowered for 10%), the actual lift of +43.09% was large enough to achieve power ($1 - \beta \approx 1.0$)[cite: 2].
* **Segment Robustness:** Conversion gains held across all 7 days of the week, with 5 of 7 days showing significant positive lift after Benjamini-Hochberg FDR correction ($q < 0.05$)[cite: 2].

---

## 3. Peeking Simulation & Experimentation Risks

Continuous daily re-testing demonstrated that nominal p-values dropped below $0.05$ on Day 1[cite: 2]. However, the observed relative lift was unstable in early windows ($+47.4\%$ on Day 1, $+69.1\%$ on Day 2) before settling at $+43.1\%$ as the sample grew to 588k[cite: 2]. 

Stopping tests at the first point of significance inflates false positive rates and overestimates effect magnitude. All future marketing experiments should enforce pre-calculated fixed sample sizes or sequential alpha-spending boundaries (e.g., O'Brien-Fleming)[cite: 2].

---

## 4. Business Caveats & Limitations

1. **No Revenue/Spend Data:** The dataset records conversions as binary events[cite: 2]. We cannot compute ROAS or marginal customer acquisition cost (CAC).
2. **Post-Treatment Total Ads Bias:** Users who convert may browse longer, increasing total ads viewed. As a result, ad frequency is partially endogenous and cannot be interpreted as a clean causal exposure curve.
3. **Rollout Approximation:** Exposure days represent the mode of user views (`most ads day`), serving as a proxy rather than an exact transaction timestamp log[cite: 2].

---

## 5. Next Steps
* Deploy ad traffic allocation to 100%[cite: 2].
* Integrate cart value and advertising impression costs to transition from conversion rate tracking to net revenue tracking[cite: 2].
