# Marketing A/B Test Analysis — Ad vs. PSA Conversion Lift

End-to-end statistical analysis of a real marketing A/B test: power
analysis, significance testing with confidence intervals, segment-level
(Simpson's paradox) checks, and a simulation showing the false-positive
risk of "peeking" at results early.

**Dataset:** Kaggle "Marketing A/B Testing" — download into `data/raw/marketing_AB.csv`
(not committed — see .gitignore).

## Quick start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# place marketing_AB.csv in data/raw/
python src/power_analysis.py
python src/run_test.py
python src/segment_analysis.py
python src/peeking_simulation.py
pytest tests/
```

## Build log
- [ ] Day 1: setup, EDA, power analysis
- [ ] Day 2: significance test, SRM check, segment analysis, peeking simulation
- [ ] Day 3: insights memo, production polish, GitHub push
