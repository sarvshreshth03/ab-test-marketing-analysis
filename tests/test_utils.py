import numpy as np
import pytest
from src.utils import (
    calculate_two_proportion_ztest,
    calculate_lift_and_ci,
    calculate_sample_ratio_mismatch,
    calculate_required_sample_size,
)


def test_two_proportion_ztest_identical():
    z_stat, p_val = calculate_two_proportion_ztest((50, 50), (1000, 1000))
    assert pytest.approx(z_stat, abs=1e-4) == 0.0
    assert pytest.approx(p_val, abs=1e-4) == 1.0


def test_two_proportion_ztest_significant():
    z_stat, p_val = calculate_two_proportion_ztest((100, 50), (1000, 1000))
    assert z_stat > 0
    assert p_val < 0.001


def test_calculate_lift_and_ci():
    lift_stats = calculate_lift_and_ci(
        p_treatment=0.10,
        p_control=0.08,
        n_treatment=1000,
        n_control=1000,
    )
    assert pytest.approx(lift_stats["abs_lift"], abs=1e-4) == 0.02
    assert pytest.approx(lift_stats["rel_lift"], abs=1e-4) == 0.25
    assert lift_stats["abs_ci"][0] < lift_stats["abs_lift"] < lift_stats["abs_ci"][1]


def test_calculate_sample_ratio_mismatch_clean():
    chi2, p_val = calculate_sample_ratio_mismatch(
        observed_counts=(500, 500),
        expected_ratio=(0.5, 0.5),
    )
    assert pytest.approx(chi2, abs=1e-4) == 0.0
    assert pytest.approx(p_val, abs=1e-4) == 1.0


def test_calculate_sample_ratio_mismatch_detected():
    chi2, p_val = calculate_sample_ratio_mismatch(
        observed_counts=(600, 400),
        expected_ratio=(0.5, 0.5),
    )
    assert p_val < 0.001


def test_calculate_required_sample_size():
    n_req = calculate_required_sample_size(
        baseline_rate=0.02,
        mde_relative=0.10,
        alpha=0.05,
        power=0.80,
        ratio=1.0,
    )
    assert n_req > 10000
