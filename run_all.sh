#!/usr/bin/env bash
set -euo pipefail

echo "========================================="
echo "Running Test Suite (pytest)"
echo "========================================="
pytest -v

echo ""
echo "========================================="
echo "1. Power Analysis & EDA"
echo "========================================="
python -m src.power_analysis

echo ""
echo "========================================="
echo "2. Two-Proportion z-test & SRM Check"
echo "========================================="
python -m src.run_test

echo ""
echo "========================================="
echo "3. Segment Analysis (Simpson's Paradox)"
echo "========================================="
python -m src.segment_analysis

echo ""
echo "========================================="
echo "4. Peeking Simulation"
echo "========================================="
python -m src.peeking_simulation

echo ""
echo "Pipeline execution completed successfully."
