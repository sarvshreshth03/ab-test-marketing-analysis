# Methodology & Statistical Framework

| Step | Test / Method | Implementation | Why Chosen & Assumptions |
|---|---|---|---|
| **Power Analysis** | Normal approximation for two independent proportions | `statsmodels.stats.power.NormalIndPower` | Calculates sensitivity given baseline rate ($p=1.785\%$) and severe 24:1 allocation imbalance ($n_{ad} / n_{psa} \approx 24.0$). Confirms sample requirement for 10% MDE. |
| **Main Significance Test** | Two-proportion pooled z-test | `statsmodels.stats.proportion.proportions_ztest` | Evaluates $H_0: p_{ad} - p_{psa} = 0$ for large-sample binary conversion outcomes. Success-failure condition ($np \ge 10, n(1-p) \ge 10$) is satisfied across both variants[cite: 2]. |
| **Effect Size & Uncertainty** | Absolute and relative lift with 95% Wald CI | Custom formulation via `src/utils.py` | Reporting p-values alone masks commercial impact; confidence intervals provide bounds ($[+33.33\%, +52.84\%]$ relative lift)[cite: 2]. |
| **Sample Ratio Mismatch (SRM)** | Chi-square ($\chi^2$) goodness-of-fit test | `scipy.stats.chisquare` | Pre-condition sanity check testing observed allocation against the planned 96:4 split ($\chi^2=0.0000, p=0.9998$) to detect bucket assignment bugs[cite: 2]. |
| **Segment Analysis** | Subgroup two-proportion z-tests + Benjamini-Hochberg (FDR) | `statsmodels.stats.multitest.multipletests(method='fdr_bh')` | Verifies directional consistency across exposure days (checks for Simpson's paradox) while controlling family-wise false discovery rate across 7 simultaneous tests[cite: 2]. |
| **Peeking Simulation** | Cumulative sequential re-testing | Iterative proportion z-tests over progressive cohort cutoffs | Empirically illustrates effect size estimation instability and explains the necessity of fixed horizons or alpha-spending boundaries (e.g., O'Brien-Fleming)[cite: 2]. |
