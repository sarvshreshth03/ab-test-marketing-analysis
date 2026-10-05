"""Day 2: Segment analysis and Simpson's Paradox check with FDR correction."""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.multitest import multipletests

from src.utils import calculate_lift_and_ci, calculate_two_proportion_ztest

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATA_PATH = Path("data/raw/marketing_AB.csv")
FIGURES_PATH = Path("reports/figures")


def main():
    if not DATA_PATH.exists():
        logger.error("Dataset not found at %s", DATA_PATH)
        return

    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    segments = sorted(df["most ads day"].dropna().unique())
    logger.info("Analyzing %d segments by 'most ads day'...", len(segments))

    records = []
    for day in segments:
        sub = df[df["most ads day"] == day]
        stats = sub.groupby("test group")["converted"].agg(["count", "sum"])

        if "ad" not in stats.index or "psa" not in stats.index:
            logger.warning("Segment '%s' missing variant group, skipping.", day)
            continue

        n_ad, x_ad = int(stats.loc["ad", "count"]), int(stats.loc["ad", "sum"])
        n_psa, x_psa = int(stats.loc["psa", "count"]), int(stats.loc["psa", "sum"])

        if x_ad == 0 or x_psa == 0:
            logger.warning("Zero conversions in segment '%s', skipping.", day)
            continue

        p_ad = x_ad / n_ad
        p_psa = x_psa / n_psa

        z_stat, p_val = calculate_two_proportion_ztest((x_ad, x_psa), (n_ad, n_psa))
        lift_data = calculate_lift_and_ci(p_ad, p_psa, n_ad, n_psa)

        records.append({
            "segment": day,
            "n_ad": n_ad,
            "n_psa": n_psa,
            "p_ad": p_ad,
            "p_psa": p_psa,
            "rel_lift": lift_data["rel_lift"],
            "ci_lower": lift_data["rel_ci"][0],
            "ci_upper": lift_data["rel_ci"][1],
            "raw_pval": p_val,
        })

    seg_df = pd.DataFrame(records)

    # Benjamini-Hochberg FDR correction
    rejected, corrected_pvals, _, _ = multipletests(seg_df["raw_pval"], alpha=0.05, method="fdr_bh")
    seg_df["fdr_pval"] = corrected_pvals
    seg_df["significant"] = rejected

    logger.info("Segment breakdown results:\n%s",
                seg_df[["segment", "rel_lift", "raw_pval", "fdr_pval", "significant"]].to_string(index=False))

    # Forest plot of relative lift across segments
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(9, 5))
    y_pos = np.arange(len(seg_df))

    plt.errorbar(
        x=seg_df["rel_lift"] * 100,
        y=y_pos,
        xerr=[
            (seg_df["rel_lift"] - seg_df["ci_lower"]) * 100,
            (seg_df["ci_upper"] - seg_df["rel_lift"]) * 100,
        ],
        fmt='o',
        color='navy',
        ecolor='royalblue',
        elinewidth=2,
        capsize=4,
    )
    plt.axvline(0, color='red', linestyle='--', linewidth=1, label="No Lift (0%)")
    plt.yticks(y_pos, seg_df["segment"])
    plt.xlabel("Relative Lift (%) with 95% Confidence Interval")
    plt.ylabel("Day of Week (Most Ads Seen)")
    plt.title("Segment Forest Plot: Ad vs PSA Conversion Lift by Day")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "forest_plot_day.png", dpi=300)
    plt.close()
    logger.info("Forest plot saved to %s/forest_plot_day.png", FIGURES_PATH)


if __name__ == "__main__":
    main()
