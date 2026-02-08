"""CLI for the single-EV droplet occupancy calculator."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .core import (
    compare_operating_points,
    expected_interpretable_single_events,
    lambda_confidence_interval_from_empty_counts,
    occupancy_metrics,
    required_droplets_for_target_events,
)


def _fmt(x: float) -> str:
    return f"{x:.6f}"


def _summary(args: argparse.Namespace) -> int:
    m = occupancy_metrics(args.lambda_value)
    payload = {
        "lambda": m.lambda_value,
        "p_empty": m.p_empty,
        "p_single": m.p_single,
        "p_multi_ge_2": m.p_multi_ge_2,
        "purity_given_occupied": m.purity_given_occupied,
    }

    if args.n_droplets is not None:
        payload["expected_interpretable_single_events"] = expected_interpretable_single_events(
            n_droplets=args.n_droplets,
            lambda_value=args.lambda_value,
            q_qc=args.q_qc,
            q_identity=args.q_identity,
        )

    if args.empty_count is not None and args.total_count is not None:
        ci = lambda_confidence_interval_from_empty_counts(
            n_empty=args.empty_count,
            n_total=args.total_count,
            confidence=args.confidence,
        )
        payload["lambda_ci"] = asdict(ci)

    if args.json:
        print(json.dumps(payload, indent=2))
        return 0

    print(f"lambda: {_fmt(payload['lambda'])}")
    print(f"P_empty: {_fmt(payload['p_empty'])}")
    print(f"P_single: {_fmt(payload['p_single'])}")
    print(f"P_multi>=2: {_fmt(payload['p_multi_ge_2'])}")
    print(f"Purity_given_occupied: {_fmt(payload['purity_given_occupied'])}")
    if "expected_interpretable_single_events" in payload:
        print(
            "Expected interpreted single events: "
            f"{_fmt(payload['expected_interpretable_single_events'])}"
        )
    if "lambda_ci" in payload:
        ci = payload["lambda_ci"]
        print(
            f"Lambda {int(args.confidence * 100)}% CI from empty counts: "
            f"[{_fmt(ci['lower'])}, {_fmt(ci['upper'])}]"
        )
    return 0


def _compare(args: argparse.Namespace) -> int:
    c = compare_operating_points(args.lambda_a, args.lambda_b)
    if args.json:
        print(json.dumps(asdict(c), indent=2))
        return 0
    print(f"lambda_a: {_fmt(c.lambda_a)}")
    print(f"lambda_b: {_fmt(c.lambda_b)}")
    print(f"Single-event yield ratio (b/a): {_fmt(c.single_yield_ratio_b_over_a)}")
    print(f"Multiplet burden ratio (b/a): {_fmt(c.multi_burden_ratio_b_over_a)}")
    return 0


def _plan(args: argparse.Namespace) -> int:
    n_required = required_droplets_for_target_events(
        target_interpretable_single_events=args.target_single_events,
        lambda_value=args.lambda_value,
        q_qc=args.q_qc,
        q_identity=args.q_identity,
    )
    payload = {"required_droplets": n_required}
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print(f"Required droplets: {_fmt(n_required)}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="evdroplet",
        description="Single-EV droplet occupancy calculator",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_summary = sub.add_parser("summary", help="Compute occupancy summary for one lambda")
    p_summary.add_argument("--lambda", dest="lambda_value", type=float, required=True)
    p_summary.add_argument("--n-droplets", type=float, default=None)
    p_summary.add_argument("--q-qc", type=float, default=1.0)
    p_summary.add_argument("--q-identity", type=float, default=1.0)
    p_summary.add_argument("--empty-count", type=int, default=None)
    p_summary.add_argument("--total-count", type=int, default=None)
    p_summary.add_argument("--confidence", type=float, default=0.95)
    p_summary.add_argument("--json", action="store_true")
    p_summary.set_defaults(func=_summary)

    p_compare = sub.add_parser("compare", help="Compare two lambda operating points")
    p_compare.add_argument("--lambda-a", type=float, required=True)
    p_compare.add_argument("--lambda-b", type=float, required=True)
    p_compare.add_argument("--json", action="store_true")
    p_compare.set_defaults(func=_compare)

    p_plan = sub.add_parser("plan", help="Plan droplet count for a target event count")
    p_plan.add_argument("--target-single-events", type=float, required=True)
    p_plan.add_argument("--lambda", dest="lambda_value", type=float, required=True)
    p_plan.add_argument("--q-qc", type=float, default=1.0)
    p_plan.add_argument("--q-identity", type=float, default=1.0)
    p_plan.add_argument("--json", action="store_true")
    p_plan.set_defaults(func=_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

