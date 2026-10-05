"""Day 2: Main significance testing, lift estimation, and SRM check."""

import logging
from pathlib import Path
import pandas as pd

from src.utils import (
    calculate_two_proportion_ztest,
    calculate_lift_and_ci,
    calculate_sample_ratio_mismatch,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_PATH = Path("data/raw/marketing_AB.csv")
ALPHA = 0.05


def main():
    if not DATA_PATH.exists():
        logger.error("Dataset not found at %s", DATA_PATH)
        return

    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Aggregate counts
    conv_table = df.groupby("test group")["converted"].agg(["count", "sum"])
    n_ad, x_ad = int(conv_table.loc["ad", "count"]), int(conv_table.loc["ad", "sum"])
    n_psa, x_psa = int(conv_table.loc["psa", "count"]), int(conv_table.loc["psa", "sum"])

    p_ad = x_ad / n_ad
    p_psa = x_psa / n_psa

    logger.info("Ad group:   %d conversions / %d users (CR: %.4f%%)", x_ad, n_ad, p_ad * 100)
    logger.info("PSA group:  %d conversions / %d users (CR: %.4f%%)", x_psa, n_psa, p_psa * 100)

    # 1. Main significance test (Two-proportion z-test)
    z_stat, p_val = calculate_two_proportion_ztest(
        successes=(x_ad, x_psa),
        nobs=(n_ad, n_psa),
        alternative="two-sided",
    )
    logger.info("Two-proportion z-test: z = %.4f, p-value = %.4e", z_stat, p_val)

    # 2. Lift and Confidence Intervals
    lift_results = calculate_lift_and_ci(
        p_treatment=p_ad,
        p_control=p_psa,
        n_treatment=n_ad,
        n_control=n_psa,
        alpha=ALPHA,
    )
    abs_lift = lift_results["abs_lift"]
    abs_ci = lift_results["abs_ci"]
    rel_lift = lift_results["rel_lift"]
    rel_ci = lift_results["rel_ci"]

    logger.info("Absolute Lift: +%.4f percentage points (95%% CI: [%.4f, %.4f])",
                abs_lift * 100, abs_ci[0] * 100, abs_ci[1] * 100)
    logger.info("Relative Lift: +%.2f%% (95%% CI: [%.2f%%, %.2f%%])",
                rel_lift * 100, rel_ci[0] * 100, rel_ci[1] * 100)

    # 3. Sample Ratio Mismatch (SRM) check
    # Expected allocation is 96.0% ad vs 4.0% psa
    chi2, p_srm = calculate_sample_ratio_mismatch(
        observed_counts=(n_ad, n_psa),
        expected_ratio=(0.96, 0.04),
    )
    logger.info("SRM Check (expected 96:4 split): Chi2 = %.4f, p-value = %.4f", chi2, p_srm)
    if p_srm < 0.01:
        logger.warning("SRM ALERT: Traffic split diverges significantly from 96:4 expectation!")
    else:
        logger.info("SRM check passed: No evidence of assignment bias.")


if __name__ == "__main__":
    main()
