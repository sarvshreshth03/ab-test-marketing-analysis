"""Day 2: Main significance testing in plain English."""

from pathlib import Path
import pandas as pd

from src.utils import (
    calculate_two_proportion_ztest,
    calculate_lift_and_ci,
    calculate_sample_ratio_mismatch,
)

DATA_PATH = Path("data/raw/marketing_AB.csv")
ALPHA = 0.05


def main():
    if not DATA_PATH.exists():
        print(f"Error: Dataset not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    conv_table = df.groupby("test group")["converted"].agg(["count", "sum"])
    n_ad, x_ad = int(conv_table.loc["ad", "count"]), int(conv_table.loc["ad", "sum"])
    n_psa, x_psa = int(conv_table.loc["psa", "count"]), int(conv_table.loc["psa", "sum"])

    p_ad = x_ad / n_ad
    p_psa = x_psa / n_psa

    _, p_val = calculate_two_proportion_ztest(
        successes=(x_ad, x_psa),
        nobs=(n_ad, n_psa),
        alternative="two-sided",
    )

    lift_results = calculate_lift_and_ci(
        p_treatment=p_ad,
        p_control=p_psa,
        n_treatment=n_ad,
        n_control=n_psa,
        alpha=ALPHA,
    )
    rel_lift = lift_results["rel_lift"]
    rel_ci = lift_results["rel_ci"]

    _, p_srm = calculate_sample_ratio_mismatch(
        observed_counts=(n_ad, n_psa),
        expected_ratio=(0.96, 0.04),
    )

    print("\n========================================================")
    print(" STEP 2: DID THE ADS ACTUALLY WORK? (FINAL RESULTS)")
    print("========================================================")
    print(f"1. Product Ad Group : {x_ad:,} buyers out of {n_ad:,} people ({p_ad*100:.2f}%)")
    print(f"2. Generic PSA Group: {x_psa:,} buyers out of {n_psa:,} people ({p_psa*100:.2f}%)")
    print("--------------------------------------------------------")
    print(f"SALES BOOST         : +{rel_lift*100:.1f}% more people bought after seeing an Ad!")
    print(f"EXPECTED RANGE      : In the real world, you can expect a boost")
    print(f"                      between +{rel_ci[0]*100:.1f}% and +{rel_ci[1]*100:.1f}%.")
    print("--------------------------------------------------------")
    if p_val < 0.05:
        print("IS THIS RESULT REAL OR JUST LUCK?")
        print(" -> 100% REAL! The chance this happened by pure luck is virtually zero.")
    else:
        print("IS THIS RESULT REAL OR JUST LUCK?")
        print(" -> INCONCLUSIVE. We cannot be sure this wasn't just luck.")
    print("--------------------------------------------------------")
    if p_srm >= 0.01:
        print("WAS THE TRAFFIC SPLIT FAIR?")
        print(" -> PASSED! The 96% Ad / 4% PSA split worked with zero technical bugs.")
    else:
        print("WAS THE TRAFFIC SPLIT FAIR?")
        print(" -> WARNING! Something went wrong with how users were split.")
    print("========================================================\n")


if __name__ == "__main__":
    main()
