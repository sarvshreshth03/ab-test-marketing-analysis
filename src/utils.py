"""Shared statistics helper functions for the A/B test analysis."""

from typing import Tuple, Dict, Any
import numpy as np
from scipy.stats import chisquare
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import (
    proportion_confint,
    proportion_effectsize,
    proportions_ztest,
)


def calculate_two_proportion_ztest(
    successes: Tuple[int, int],
    nobs: Tuple[int, int],
    alternative: str = "two-sided",
) -> Tuple[float, float]:
    """Perform a two-proportion z-test between control and treatment.

    Parameters
    ----------
    successes : tuple of (int, int)
        (treatment_successes, control_successes)
    nobs : tuple of (int, int)
        (treatment_total, control_total)
    alternative : str, default='two-sided'
        Alternative hypothesis ('two-sided', 'larger', 'smaller').

    Returns
    -------
    z_stat : float
    p_value : float
    """
    z_stat, p_val = proportions_ztest(
        count=list(successes),
        nobs=list(nobs),
        alternative=alternative,
    )
    return float(z_stat), float(p_val)


def calculate_lift_and_ci(
    p_treatment: float,
    p_control: float,
    n_treatment: int,
    n_control: int,
    alpha: float = 0.05,
) -> Dict[str, Any]:
    """Calculate absolute and relative lift with confidence intervals."""
    abs_lift = p_treatment - p_control
    rel_lift = (abs_lift / p_control) if p_control > 0 else np.nan

    se_diff = np.sqrt(
        (p_treatment * (1 - p_treatment) / n_treatment)
        + (p_control * (1 - p_control) / n_control)
    )
    z_crit = 1.95996  # Standard two-sided 95% critical value

    abs_ci_lower = abs_lift - z_crit * se_diff
    abs_ci_upper = abs_lift + z_crit * se_diff

    rel_ci_lower = (abs_ci_lower / p_control) if p_control > 0 else np.nan
    rel_ci_upper = (abs_ci_upper / p_control) if p_control > 0 else np.nan

    treatment_ci = proportion_confint(
        count=int(round(p_treatment * n_treatment)),
        nobs=n_treatment,
        alpha=alpha,
        method="normal",
    )
    control_ci = proportion_confint(
        count=int(round(p_control * n_control)),
        nobs=n_control,
        alpha=alpha,
        method="normal",
    )

    return {
        "abs_lift": abs_lift,
        "abs_ci": (abs_ci_lower, abs_ci_upper),
        "rel_lift": rel_lift,
        "rel_ci": (rel_ci_lower, rel_ci_upper),
        "treatment_ci": treatment_ci,
        "control_ci": control_ci,
    }


def calculate_sample_ratio_mismatch(
    observed_counts: Tuple[int, int],
    expected_ratio: Tuple[float, float],
) -> Tuple[float, float]:
    """Perform a Chi-square goodness-of-fit test to detect Sample Ratio Mismatch (SRM)."""
    total = sum(observed_counts)
    expected_counts = [total * r for r in expected_ratio]
    chi2, p_val = chisquare(f_obs=observed_counts, f_exp=expected_counts)
    return float(chi2), float(p_val)


def calculate_required_sample_size(
    baseline_rate: float,
    mde_relative: float,
    alpha: float = 0.05,
    power: float = 0.80,
    ratio: float = 1.0,
) -> float:
    """Calculate required sample size for the control group given an MDE and allocation ratio."""
    treatment_rate = baseline_rate * (1 + mde_relative)
    effect_size = proportion_effectsize(treatment_rate, baseline_rate)
    analysis = NormalIndPower()
    n_control = analysis.solve_power(
        effect_size=effect_size,
        alpha=alpha,
        power=power,
        ratio=ratio,
        alternative="two-sided",
    )
    return float(n_control)