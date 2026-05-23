#!/usr/bin/env python3
"""Reproduce the Table 5 (Ablation) CIs in the paper.

Usage:
    python3 reproduce_ablation_ci.py

Reads ablation_results.json (in this directory) and prints:
  - Wilson 95% CI on the "checks-defect-free" rate for each condition (A/B/C)
  - Per-case mean pass rate with paired-bootstrap 95% CI (n=25 cases)
  - Paired-bootstrap 95% CI on the per-case delta B - C and A - B

Seed: 42. Resamples: 10,000. Python 3.11.
"""

import json
import math
import random
import sys
from pathlib import Path

random.seed(42)
N_BOOTSTRAP = 10_000


def wilson_ci(k: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = k / n
    z = 1.959963984540054
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return center - half, center + half


def bootstrap_mean_ci(vals: list[float], n: int = N_BOOTSTRAP) -> tuple[float, float, float]:
    L = len(vals)
    means: list[float] = []
    for _ in range(n):
        s = sum(vals[random.randrange(L)] for _ in range(L))
        means.append(s / L)
    means.sort()
    mean = sum(vals) / L
    return mean, means[int(0.025 * n)], means[int(0.975 * n)]


def paired_bootstrap_delta(a: list[float], b: list[float], n: int = N_BOOTSTRAP) -> tuple[float, float, float]:
    L = len(a)
    deltas: list[float] = []
    for _ in range(n):
        idx = [random.randrange(L) for _ in range(L)]
        da = sum(a[i] for i in idx) / L
        db = sum(b[i] for i in idx) / L
        deltas.append(db - da)
    deltas.sort()
    point = sum(b) / L - sum(a) / L
    return point, deltas[int(0.025 * n)], deltas[int(0.975 * n)]


def main() -> int:
    here = Path(__file__).parent
    src = here / "ablation_results.json"
    if not src.exists():
        print(f"missing: {src}", file=sys.stderr)
        return 1
    data = json.loads(src.read_text())
    conds: dict[str, dict] = {r["name"][0]: r for r in data["results"]}

    print("=== Wilson 95% CI on 'checks-defect-free' rate (n=282 checks) ===")
    for k in ["C", "B", "A"]:
        r = conds[k]
        passing = r["totalChecks"] - r["failingChecks"]
        lo, hi = wilson_ci(passing, r["totalChecks"])
        print(f"  {r['name']}: {passing}/{r['totalChecks']} = {passing/r['totalChecks']*100:.1f}%  95% CI ({lo*100:.1f}, {hi*100:.1f})%")

    print("\n=== Per-case mean pass rate, bootstrap 95% CI (n=25 cases) ===")
    rates_by_cond = {}
    for k in ["C", "B", "A"]:
        rates = [c / 282 for c in conds[k]["perNotePassCounts"]]
        rates_by_cond[k] = rates
        mean, lo, hi = bootstrap_mean_ci(rates)
        print(f"  {conds[k]['name']}: {mean*100:.1f}%  95% CI ({lo*100:.1f}, {hi*100:.1f})%")

    print("\n=== Paired-bootstrap delta CIs (n=25 cases) ===")
    point, lo, hi = paired_bootstrap_delta(rates_by_cond["C"], rates_by_cond["B"])
    print(f"  B − C delta: {point*100:+.2f} pp  95% CI ({lo*100:+.2f}, {hi*100:+.2f}) pp")
    point, lo, hi = paired_bootstrap_delta(rates_by_cond["B"], rates_by_cond["A"])
    print(f"  A − B delta: {point*100:+.2f} pp  95% CI ({lo*100:+.2f}, {hi*100:+.2f}) pp")

    print("\nDone. These are the numbers reported in Table 5 and §8 of the paper.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
