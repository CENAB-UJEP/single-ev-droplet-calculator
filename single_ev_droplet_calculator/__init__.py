"""Single-EV droplet occupancy calculator."""

from .core import (
    ComparisonMetrics,
    OccupancyMetrics,
    WilsonInterval,
    compare_operating_points,
    dual_any_multi_probability,
    dual_single_pair_probability,
    expected_interpretable_single_events,
    lambda_confidence_interval_from_empty_counts,
    lambda_from_empty_fraction,
    occupancy_metrics,
    required_droplets_for_target_events,
)

__all__ = [
    "ComparisonMetrics",
    "OccupancyMetrics",
    "WilsonInterval",
    "occupancy_metrics",
    "lambda_from_empty_fraction",
    "lambda_confidence_interval_from_empty_counts",
    "expected_interpretable_single_events",
    "required_droplets_for_target_events",
    "compare_operating_points",
    "dual_single_pair_probability",
    "dual_any_multi_probability",
]

