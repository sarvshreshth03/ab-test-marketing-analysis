"""Day 2: Peeking simulation demonstrating alpha-inflation and p-value instability."""

import logging
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest

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

    # Approximate timeline sequencing using 'most ads day'
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    available_days = [d for d in day_order if d in df["most ads day"].unique()]

    logger.info("Simulating cumulative peeking over sequential days: %s", available_days)

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
                "step": f"Up to {day}",
                "total_users": len(subset),
                "p_val": p_val,
                "rel_lift": rel_lift,
            })

    peek_df = pd.DataFrame(results)
    logger.info("Peeking progression table:\n%s", peek_df.to_string(index=False))

    # Visualization: p-value trajectory against significance boundary
    FIGURES_PATH.mkdir(parents=True, exist_ok=True)
    fig, ax1 = plt.subplots(figsize=(9, 4.5))

    ax1.plot(peek_df["step"], peek_df["p_val"], marker='o', color='crimson', linewidth=2, label="Calculated p-value")
    ax1.axhline(0.05, color='black', linestyle='--', label=r"Nominal $\alpha = 0.05$")
    ax1.set_ylabel("p-value", color='crimson')
    ax1.tick_params(axis='y', labelcolor='crimson')
    ax1.set_xticklabels(peek_df["step"], rotation=25, ha="right")
    ax1.set_title("Sequential Peeking Simulation: Cumulative p-value Trajectory")

    ax2 = ax1.twinx()
    ax2.plot(peek_df["step"], peek_df["rel_lift"] * 100, marker='s', color='teal', linestyle=':', label="Relative Lift (%)")
    ax2.set_ylabel("Relative Lift (%)", color='teal')
    ax2.tick_params(axis='y', labelcolor='teal')

    fig.tight_layout()
    plt.savefig(FIGURES_PATH / "peeking_simulation.png", dpi=300)
    plt.close()
    logger.info("Peeking simulation chart saved to %s/peeking_simulation.png", FIGURES_PATH)


if __name__ == "__main__":
    main()
