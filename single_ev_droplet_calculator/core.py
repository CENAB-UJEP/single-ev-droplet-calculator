"""Core math for Poisson occupancy-aware single-EV droplet planning."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, log, sqrt
from statistics import NormalDist


@dataclass(frozen=True)
class OccupancyMetrics:
    lambda_value: float
    p_empty: float
    p_single: float
    p_multi_ge_2: float
    purity_given_occupied: float


@dataclass(frozen=True)
class WilsonInterval:
    lower: float
    upper: float
    confidence: float


@dataclass(frozen=True)
class ComparisonMetrics:
    lambda_a: float
    lambda_b: float
    single_yield_ratio_b_over_a: float
    multi_burden_ratio_b_over_a: float


def _validate_lambda(lambda_value: float) -> None:
    if lambda_value < 0:
        raise ValueError("lambda_value must be >= 0.")


def _validate_fraction(name: str, value: float) -> None:
    if not (0.0 <= value <= 1.0):
        raise ValueError(f"{name} must be in [0, 1].")


def occupancy_metrics(lambda_value: float) -> OccupancyMetrics:
    """Compute occupancy metrics from Poisson loading parameter."""
    _validate_lambda(lambda_value)
    p_empty = exp(-lambda_value)
    p_single = lambda_value * p_empty
    p_multi = 1.0 - p_empty - p_single
    occupied = 1.0 - p_empty
    purity = p_single / occupied if occupied > 0 else 0.0
    return OccupancyMetrics(
        lambda_value=lambda_value,
        p_empty=p_empty,
        p_single=p_single,
        p_multi_ge_2=p_multi,
        purity_given_occupied=purity,
    )


def lambda_from_empty_fraction(f_empty: float) -> float:
    """Estimate lambda from empty-droplet fraction: lambda = -ln(f_empty)."""
    if not (0.0 < f_empty < 1.0):
        raise ValueError("f_empty must be strictly between 0 and 1.")
    return -log(f_empty)


def wilson_interval(
    k_success: int,
    n_total: int,
    confidence: float = 0.95,
) -> WilsonInterval:
    """Wilson score interval for a binomial proportion."""
    if n_total <= 0:
        raise ValueError("n_total must be > 0.")
    if not (0 <= k_success <= n_total):
        raise ValueError("k_success must be in [0, n_total].")
    if not (0.0 < confidence < 1.0):
        raise ValueError("confidence must be in (0, 1).")

    p_hat = k_success / n_total
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    z2 = z * z

    denom = 1.0 + z2 / n_total
    center = (p_hat + z2 / (2.0 * n_total)) / denom
    half = (
        z
        * sqrt((p_hat * (1.0 - p_hat) / n_total) + (z2 / (4.0 * n_total * n_total)))
        / denom
    )
    lower = max(0.0, center - half)
    upper = min(1.0, center + half)
    return WilsonInterval(lower=lower, upper=upper, confidence=confidence)


def lambda_confidence_interval_from_empty_counts(
    n_empty: int,
    n_total: int,
    confidence: float = 0.95,
) -> WilsonInterval:
    """Propagate Wilson interval on f_empty into a lambda interval."""
    interval = wilson_interval(n_empty, n_total, confidence)

    # lambda = -ln(f_empty); monotonic decreasing in f_empty
    # lower lambda comes from upper f_empty and vice versa.
    eps = 1e-12
    f_lo = max(interval.lower, eps)
    f_hi = min(interval.upper, 1.0 - eps)

    lam_lower = -log(f_hi)
    lam_upper = -log(f_lo)
    return WilsonInterval(lower=lam_lower, upper=lam_upper, confidence=confidence)


def expected_interpretable_single_events(
    n_droplets: float,
    lambda_value: float,
    q_qc: float = 1.0,
    q_identity: float = 1.0,
) -> float:
    """Expected interpreted single-EV events after QC and identity filters."""
    if n_droplets < 0:
        raise ValueError("n_droplets must be >= 0.")
    _validate_fraction("q_qc", q_qc)
    _validate_fraction("q_identity", q_identity)

    p_single = occupancy_metrics(lambda_value).p_single
    return n_droplets * p_single * q_qc * q_identity


def required_droplets_for_target_events(
    target_interpretable_single_events: float,
    lambda_value: float,
    q_qc: float = 1.0,
    q_identity: float = 1.0,
) -> float:
    """Droplet count needed for target interpreted single-EV events."""
    if target_interpretable_single_events <= 0:
        raise ValueError("target_interpretable_single_events must be > 0.")
    _validate_fraction("q_qc", q_qc)
    _validate_fraction("q_identity", q_identity)

    effective = occupancy_metrics(lambda_value).p_single * q_qc * q_identity
    if effective <= 0:
        raise ValueError("Effective interpreted-event probability must be > 0.")
    return target_interpretable_single_events / effective


def compare_operating_points(lambda_a: float, lambda_b: float) -> ComparisonMetrics:
    """Compare throughput and multiplet burden ratios for two lambda settings."""
    m_a = occupancy_metrics(lambda_a)
    m_b = occupancy_metrics(lambda_b)
    if m_a.p_single <= 0:
        raise ValueError("lambda_a must yield a positive single-event probability.")
    if m_a.p_multi_ge_2 <= 0:
        raise ValueError("lambda_a must yield a positive multiplet probability.")

    return ComparisonMetrics(
        lambda_a=lambda_a,
        lambda_b=lambda_b,
        single_yield_ratio_b_over_a=m_b.p_single / m_a.p_single,
        multi_burden_ratio_b_over_a=m_b.p_multi_ge_2 / m_a.p_multi_ge_2,
    )


def dual_single_pair_probability(lambda_a: float, lambda_b: float) -> float:
    """Probability of exactly one entity from each independent Poisson channel."""
    _validate_lambda(lambda_a)
    _validate_lambda(lambda_b)
    return (lambda_a * exp(-lambda_a)) * (lambda_b * exp(-lambda_b))


def dual_any_multi_probability(lambda_a: float, lambda_b: float) -> float:
    """Probability that either independent channel has occupancy >= 2."""
    _validate_lambda(lambda_a)
    _validate_lambda(lambda_b)
    p_a_le_1 = exp(-lambda_a) * (1.0 + lambda_a)
    p_b_le_1 = exp(-lambda_b) * (1.0 + lambda_b)
    return 1.0 - (p_a_le_1 * p_b_le_1)

