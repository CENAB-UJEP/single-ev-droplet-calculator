# Single-EV Droplet Occupancy Calculator

Lightweight, tested calculator for occupancy-aware single-EV droplet assay design and reporting.

Companion code for the review manuscript:
> *Droplet microfluidics for single-extracellular-vesicle analysis* (submitted to Biotechnology and Bioengineering)

## Try it online (no install)

**Web calculator:** [https://cenab-ujep.github.io/single-ev-droplet-calculator/)
— interactive browser app with Summary, Compare, Plan tabs and a live occupancy chart.

**Colab notebook:** [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/cenab-ujep/single-ev-droplet-calculator/blob/main/examples/interactive_calculator.ipynb)
— run the Python package interactively, no local install needed.

## Scope

Implements core formulas and planning utilities for:

- Poisson occupancy metrics (`P_empty`, `P_single`, `P_multi>=2`)
- Purity among occupied droplets
- Effective interpreted-event yield after QC and identity filtering
- Required droplet count for a target number of interpreted single-EV events
- Comparison of two operating points (`lambda_a` vs `lambda_b`)
- Empty-droplet based `lambda` estimation and Wilson CI propagation
- Optional dual-entity pair occupancy (`1 EV` and `1 co-encapsulated partner`)

## Core formulas

For loading parameter `lambda`:

- `P(k) = exp(-lambda) * lambda^k / k!`
- `P_empty = exp(-lambda)`
- `P_single = lambda * exp(-lambda)`
- `P_multi>=2 = 1 - P_empty - P_single`
- `Purity_given_occupied = P_single / (1 - P_empty)`

Planning:

- `Expected_interpreted_single_events = N_droplets * P_single * q_qc * q_identity`
- `Required_droplets = Target_interpreted_single_events / (P_single * q_qc * q_identity)`

## Install

```bash
git clone https://cenab-ujep.com/MichaLie/single-ev-droplet-calculator.git
cd single-ev-droplet-calculator
python3 -m pip install -e .
```

## CLI usage

```bash
# Summary metrics for one lambda
evdroplet summary --lambda 0.10 --n-droplets 250000 --q-qc 0.6 --q-identity 0.7

# Compare two operating points
evdroplet compare --lambda-a 0.10 --lambda-b 0.20

# Plan required droplet count
evdroplet plan --target-single-events 10000 --lambda 0.10 --q-qc 0.6 --q-identity 0.7

# Estimate lambda from empty counts with CI
evdroplet summary --lambda 0.10 --empty-count 9048 --total-count 10000
```

## Manuscript anchor values (expected)

At `lambda=0.10`:

- `P_empty = 0.904837`
- `P_single = 0.090484`
- `P_multi>=2 = 0.004679`
- `Purity_given_occupied = 0.950833`

At `lambda=0.20`:

- `P_empty = 0.818731`
- `P_single = 0.163746`
- `P_multi>=2 = 0.017523`
- `Purity_given_occupied = 0.903331`

Ratios (`0.20` vs `0.10`):

- `single-event yield ratio = 1.809675`
- `multi-occupancy burden ratio = 3.745180`

## Testing

Uses Python `unittest` (no pytest dependency required):

```bash
python3 -m unittest discover -s tests -v
```

## Reproduce anchor table

```bash
python3 scripts/reproduce_anchor_table.py
```

## Files

- `single_ev_droplet_calculator/core.py` — main math functions
- `single_ev_droplet_calculator/cli.py` — command-line interface
- `tests/test_core.py` — numeric and validation tests
- `scripts/reproduce_anchor_table.py` — reproducible anchor table generator
- `examples/interactive_calculator.ipynb` — Colab notebook (zero-install demo)
- `examples/example_inputs.json` — sample CLI inputs
- `validation/` — saved CLI and test outputs for traceability

## License

MIT
