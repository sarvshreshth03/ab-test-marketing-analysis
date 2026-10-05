# Marketing A/B Test Analysis — Ad vs. PSA Conversion Lift

Production-grade statistical analysis of an A/B test with 588,101 users: power analysis accounting for class imbalance, two-proportion z-tests with confidence intervals, Benjamini-Hochberg segment analysis (Simpson's paradox check), and a peeking simulation illustrating sequential testing risks[cite: 2].

**Dataset:** Kaggle "Marketing A/B Testing" placed in `data/raw/marketing_AB.csv`[cite: 1, 2].

## Key Results Summary
- **Control (PSA) CR:** 1.785% (420 / 23,524)[cite: 2]
- **Treatment (Ad) CR:** 2.555% (14,423 / 564,577)[cite: 2]
- **Relative Lift:** **+43.09%** (95% CI: [+33.33%, +52.84%], $z = 7.37$, $p = 1.71 \times 10^{-13}$)[cite: 2]
- **SRM Check:** Clean allocation ($\chi^2 = 0.0000, p = 0.9998$)[cite: 2]
- **Segment Robustness:** Positive directional lift across all 7 days with zero reversals[cite: 2]

## Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./run_all.sh
ab-test-marketing-analysis/
├── docs/
│   ├── BRD.md
│   └── methodology.md
├── src/
│   ├── utils.py
│   ├── power_analysis.py
│   ├── run_test.py
│   ├── segment_analysis.py
│   └── peeking_simulation.py
├── tests/
│   └── test_utils.py
├── reports/
│   ├── figures/
│   └── insights_memo.md
├── run_all.sh
└── requirements.txt
