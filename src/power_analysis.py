"""Day 1: Exploratory Data Analysis & Power Analysis.

Evaluates sample sizes, baseline conversion rate, class imbalance (96/4),
and whether the test was adequately powered for a chosen relative MDE.
"""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils import calculate_required_sample_size

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Constants
DATA_PATH = Path("data/raw/marketing_AB.csv")
FIGURES_PATH = Path("reports/figures")
ALPHA = 0.05
POWER = 0.80
MDE_RELATIVE = 0.10  # 10% relative lift target


def run_eda(df: pd.DataFrame) -> None:
    """Generate and save EDA plots."""
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Conversion Rate by Group
    plt.figure(figsize=(6, 4))
    conv_by_group = df.groupby("test group")["converted"].mean().reset_index()
    ax = sns.barplot(x="test group", y="converted", data=conv_by_group, palette="Blues_d")
    plt.title("Conversion Rate by Group")
    plt.ylabel("Conversion Rate")
    plt.xlabel("Test Group")
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.4f}", (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center", va="center", xytext=(0, 5), textcoords="offset points")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "conversion_rate_by_group.png", dpi=300)
    plt.close()

    # 2. Total Ads Distribution (log scale due to right-skew)
    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x="total ads", hue="test group", bins=50, log_scale=(False, True), common_norm=False)
    plt.title("Distribution of Total Ads Seen (Log Scale)")
    plt.xlabel("Total Ads")
    plt.ylabel("Count (log)")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "total_ads_distribution.png", dpi=300)
    plt.close()

    logger.info("EDA figures successfully saved to %s", FIGURES_PATH)


def main():
    if not DATA_PATH.exists():
        logger.error("Dataset not found at %s. Please place marketing_AB.csv in data/raw/", DATA_PATH)
        return

    logger.info("Loading dataset from %s...", DATA_PATH)
    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    logger.info("Total rows: %d, columns: %s", len(df), list(df.columns))

    # Basic summaries
    group_counts = df["test group"].value_counts()
    n_ad = group_counts.get("ad", 0)
    n_psa = group_counts.get("psa", 0)
    logger.info("Sample split: ad=%d (%.2f%%), psa=%d (%.2f%%)",
                n_ad, (n_ad / len(df)) * 100, n_psa, (n_psa / len(df)) * 100)

    conv_summary = df.groupby("test group")["converted"].agg(["count", "sum", "mean"])
    logger.info("Conversion Summary:\n%s", conv_summary)

    baseline_rate = conv_summary.loc["psa", "mean"]
    ad_rate = conv_summary.loc["ad", "mean"]
    logger.info("Baseline PSA Conversion Rate: %.4f", baseline_rate)
    logger.info("Ad Conversion Rate: %.4f", ad_rate)

    # Power Analysis
    # 1:1 balanced design
    req_n_balanced = calculate_required_sample_size(
        baseline_rate=baseline_rate,
        mde_relative=MDE_RELATIVE,
        alpha=ALPHA,
        power=POWER,
        ratio=1.0,
    )
    logger.info("Required sample size per group (1:1 balanced ratio, 10%% MDE): %.0f", req_n_balanced)

    # Actual unequal ratio: ratio = n_treatment / n_control
    actual_ratio = n_ad / n_psa
    req_n_psa_actual_ratio = calculate_required_sample_size(
        baseline_rate=baseline_rate,
        mde_relative=MDE_RELATIVE,
        alpha=ALPHA,
        power=POWER,
        ratio=actual_ratio,
    )
    logger.info("Actual sample size ratio (ad / psa): %.2f", actual_ratio)
    logger.info("Required control (PSA) sample size given unequal split: %.0f", req_n_psa_actual_ratio)
    logger.info("Actual control (PSA) sample size: %d", n_psa)

    if n_psa >= req_n_psa_actual_ratio:
        logger.info("Experiment was ADEQUATELY POWERED for a %.0f%% relative MDE.", MDE_RELATIVE * 100)
    else:
        logger.warning("Experiment was UNDERPOWERED for a %.0f%% relative MDE.", MDE_RELATIVE * 100)

    # Run EDA
    run_eda(df)


if __name__ == "__main__":
    main()
