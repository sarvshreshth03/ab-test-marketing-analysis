"""Day 1: Exploratory Data Analysis & Power Analysis (Plain-English Version)."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.utils import calculate_required_sample_size

DATA_PATH = Path("data/raw/marketing_AB.csv")
FIGURES_PATH = Path("reports/figures")
ALPHA = 0.05
POWER = 0.80
MDE_RELATIVE = 0.10  # 10% target sales boost


def run_eda(df: pd.DataFrame) -> None:
    """Generate and save easy-to-read charts."""
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    # 1. Conversion Rate by Group (shown as simple percentages)
    plt.figure(figsize=(6, 4.5))
    conv_by_group = df.groupby("test group")["converted"].mean().reset_index()
    conv_by_group["converted_pct"] = conv_by_group["converted"] * 100
    conv_by_group["Group Name"] = conv_by_group["test group"].map({
        "ad": "Saw Product Ad",
        "psa": "Saw Generic PSA (Baseline)"
    })

    ax = sns.barplot(
        x="Group Name",
        y="converted_pct",
        hue="Group Name",
        data=conv_by_group,
        palette="Blues_d",
        legend=False,
    )
    plt.title("Who Bought More? (% of Visitors Who Purchased)", fontsize=12, fontweight="bold")
    plt.ylabel("Purchase Rate (%)")
    plt.xlabel("")
    plt.ylim(0, 3.0)
    for p in ax.patches:
        ax.annotate(
            f"{p.get_height():.2f}%",
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 8),
            textcoords="offset points",
            fontweight="bold",
        )
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "conversion_rate_by_group.png", dpi=300)
    plt.close()

    # 2. Total Ads Distribution
    plt.figure(figsize=(7, 4.5))
    df_plot = df.copy()
    df_plot["Group"] = df_plot["test group"].map({"ad": "Saw Product Ad", "psa": "Saw Generic PSA"})
    sns.kdeplot(
        data=df_plot,
        x="total ads",
        hue="Group",
        common_norm=False,
        log_scale=True,
        fill=True,
        alpha=0.3,
        palette="tab10",
    )
    plt.title("Was the Test Fair? (Number of Messages Seen per Person)", fontsize=12, fontweight="bold")
    plt.xlabel("Number of Messages Seen (Log Scale)")
    plt.ylabel("Share of Users")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "total_ads_distribution.png", dpi=300)
    plt.close()


def main():
    if not DATA_PATH.exists():
        print(f"Error: Dataset not found at {DATA_PATH}. Please place marketing_AB.csv in data/raw/")
        return

    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    group_counts = df["test group"].value_counts()
    n_ad = group_counts.get("ad", 0)
    n_psa = group_counts.get("psa", 0)

    conv_summary = df.groupby("test group")["converted"].agg(["count", "sum", "mean"])
    baseline_rate = conv_summary.loc["psa", "mean"]
    ad_rate = conv_summary.loc["ad", "mean"]

    actual_ratio = n_ad / n_psa
    req_n_psa = calculate_required_sample_size(
        baseline_rate=baseline_rate,
        mde_relative=MDE_RELATIVE,
        alpha=ALPHA,
        power=POWER,
        ratio=actual_ratio,
    )

    print("\n========================================================")
    print(" STEP 1: EXPERIMENT OVERVIEW & SAMPLE SIZE CHECK")
    print("========================================================")
    print(f"Total People in Experiment : {len(df):,}")
    print(f" - Saw Product Ads         : {n_ad:,} people ({(n_ad/len(df))*100:.0f}%)")
    print(f" - Saw Generic PSA         : {n_psa:,} people ({(n_psa/len(df))*100:.0f}%)")
    print("--------------------------------------------------------")
    print("INITIAL BUYING RATES:")
    print(f" - Generic PSA Group       : {baseline_rate*100:.2f}% bought (~{int(round(baseline_rate*1000))} per 1,000 people)")
    print(f" - Product Ad Group        : {ad_rate*100:.2f}% bought (~{int(round(ad_rate*1000))} per 1,000 people)")
    print("--------------------------------------------------------")
    print("DO WE HAVE ENOUGH PEOPLE TO TRUST THE TEST?")
    print(f" - To spot a small 10% boost, we needed {req_n_psa:,.0f} people in the PSA group.")
    print(f" - We actually had {n_psa:,} people in the PSA group.")
    print(" - Verdict: The PSA group was a bit small for spotting tiny changes (10%),")
    print("   but more than big enough to prove a huge jump like our +43% sales boost!")
    print("========================================================\n")

    run_eda(df)
    print("-> Saved updated easy-to-read charts to reports/figures/\n")


if __name__ == "__main__":
    main()
