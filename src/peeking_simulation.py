"""Day 2: Peeking simulation in plain English."""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

DATA_PATH = Path("data/raw/marketing_AB.csv")
FIGURES_PATH = Path("reports/figures")


def main():
    if not DATA_PATH.exists():
        print(f"Error: Dataset not found at {DATA_PATH}")
        return

    df = pd.read_csv(DATA_PATH)
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    available_days = [d for d in day_order if d in df["most ads day"].unique()]

    results = []
    cumulative_days = []

    for day in available_days:
        cumulative_days.append(day)
        subset = df[df["most ads day"].isin(cumulative_days)]
        agg = subset.groupby("test group")["converted"].agg(["count", "sum"])

        if len(agg) == 2:
            nobs = agg["count"].values
            successes = agg["sum"].values
            _, p_val = proportions_ztest(successes, nobs)

            p_ad = successes[0] / nobs[0]
            p_psa = successes[1] / nobs[1]
            rel_lift = (p_ad - p_psa) / p_psa if p_psa > 0 else 0

            results.append({
                "When We Checked": f"Up to {day}",
                "People Tested So Far": f"{len(subset):,}",
                "Estimated Sales Boost": f"+{rel_lift*100:.1f}%",
                "rel_lift_num": rel_lift * 100,
                "p_val": p_val,
            })

    peek_df = pd.DataFrame(results)

    print("\n========================================================")
    print(" STEP 4: WHY WE SHOULDN'T STOP TESTS TOO EARLY")
    print("========================================================")
    display_cols = ["When We Checked", "People Tested So Far", "Estimated Sales Boost"]
    print(peek_df[display_cols].to_string(index=False))
    print("--------------------------------------------------------")
    print("LESSON LEARNED:")
    print("If we had stopped the test on Tuesday, we would have")
    print("falsely believed ads boost sales by +69.1%!")
    print("Waiting the full week until Sunday gave us the true,")
    print("realistic number of +43.1%.")
    print("========================================================\n")

    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8.5, 4.5))
    plt.plot(
        peek_df["When We Checked"],
        peek_df["rel_lift_num"],
        marker="o",
        color="teal",
        linewidth=2.5,
        label="Estimated Sales Boost (%)",
    )
    plt.axhline(
        peek_df["rel_lift_num"].iloc[-1],
        color="crimson",
        linestyle="--",
        label=f"True Full-Week Boost (+{peek_df['rel_lift_num'].iloc[-1]:.1f}%)",
    )
    plt.ylabel("Estimated Sales Boost (%)")
    plt.xlabel("Day of the Test")
    plt.title("Why You Shouldn't Stop a Test Early: Sales Boost Over Time", fontsize=12, fontweight="bold")
    plt.xticks(rotation=20, ha="right")
    plt.ylim(35, 75)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "peeking_simulation.png", dpi=300)
    plt.close()
    print("-> Saved simplified early-peeking chart to reports/figures/peeking_simulation.png\n")


if __name__ == "__main__":
    main()
