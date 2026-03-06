#!/usr/bin/env python3
"""Reproduce the manuscript anchor table for lambda = 0.10 and 0.20.

Run from the repo root:
    python3 scripts/reproduce_anchor_table.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running from repo root without pip install
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from single_ev_droplet_calculator.core import (
    compare_operating_points,
    occupancy_metrics,
)

ANCHORS = [0.10, 0.20]


def main() -> None:
    print("=" * 62)
    print("Manuscript anchor values — Poisson occupancy metrics")
    print("=" * 62)

    for lam in ANCHORS:
        m = occupancy_metrics(lam)
        print(f"\nlambda = {lam:.2f}")
        print(f"  P_empty               = {m.p_empty:.10f}")
        print(f"  P_single              = {m.p_single:.10f}")
        print(f"  P_multi>=2            = {m.p_multi_ge_2:.10f}")
        print(f"  Purity_given_occupied = {m.purity_given_occupied:.10f}")

    c = compare_operating_points(ANCHORS[0], ANCHORS[1])
    print(f"\nRatios (lambda={ANCHORS[1]:.2f} vs {ANCHORS[0]:.2f}):")
    print(f"  Single-event yield ratio  = {c.single_yield_ratio_b_over_a:.10f}")
    print(f"  Multi-occupancy burden    = {c.multi_burden_ratio_b_over_a:.10f}")
    print()


if __name__ == "__main__":
    main()
