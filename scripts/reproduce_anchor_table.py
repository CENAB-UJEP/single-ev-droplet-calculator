from __future__ import annotations

from single_ev_droplet_calculator.core import compare_operating_points, occupancy_metrics


def main() -> None:
    print("lambda,p_empty,p_single,p_multi_ge_2,purity_given_occupied")
    for lam in [0.10, 0.20]:
        m = occupancy_metrics(lam)
        print(
            f"{lam:.2f},{m.p_empty:.6f},{m.p_single:.6f},"
            f"{m.p_multi_ge_2:.6f},{m.purity_given_occupied:.6f}"
        )

    c = compare_operating_points(0.10, 0.20)
    print()
    print(f"single_yield_ratio_0.20_vs_0.10,{c.single_yield_ratio_b_over_a:.6f}")
    print(f"multi_burden_ratio_0.20_vs_0.10,{c.multi_burden_ratio_b_over_a:.6f}")


if __name__ == "__main__":
    main()

