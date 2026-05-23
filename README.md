# Paper arXiv v1.0 — Reproducibility Bundle

This directory stages the anonymized data and analysis artifacts that reproduce the numerical results in the paper *Closed-Loop Quality Assurance for Production Clinical AI Documentation* (Napier, Wiley, Heslin; arXiv preprint, May 2026).

**Release status (2026-05-23):** staged for release. The source repository is currently private; the bundle will be released under CC BY 4.0 at a Sayvant-hosted public GitHub release and registered with a Zenodo DOI prior to peer-review submission. arXiv readers seeking the bundle before that release may contact the corresponding author (napier@stanford.edu).

## Contents

| File | Reproduces | Description |
|---|---|---|
| `ablation_results.json` | Table 5 (Ablation), §8 | Per-condition (A/B/C) pass rates with per-note pass counts (n=25 cases × 282 checks). The `perNotePassCounts` arrays drive the paired-bootstrap CIs reported in §8. |
| `ablation_omission_breakdown.json` | §8 omission analysis (5-case subsample) | Per-check categorization (fabrication / omission / other) and per-condition counts for the supplementary omission analysis. |
| `em-benchmark-bootstrap-ci.json` | §6.3(i) latency anchor | Bootstrap 95% CIs on the EM-benchmark Sayvant pipeline (n=23 cases), including the 22.0s [20.7, 23.4] latency anchor used as post-F17 operational reference. Also includes the comparator pipeline (Claude Sonnet 4.5 single-call) for reference. |

## What is NOT in this bundle

Per the §Reproducibility section of the paper, three categories are deliberately withheld:

1. **Deterministic repair-rule library content** and the full enumeration of the 282 binary checks. Operational-security reason.
2. **Per-axis numerical thresholds** in the Pareto commit rule and the severity-classification decision tree (§3.3.1). Operational-security reason.
3. **Internal prompt text** of the reasoning and assembly agents in the production pipeline. Operational-security reason.

None of these is load-bearing for the observations reported in the paper. Researchers interested in replicating the harness at a different site can do so with their own rule library and prompt text. Researchers interested in replicating the *patterns* (the four observations + F17 follow-through) can do so with the judge prompt variants in Appendix B of the paper and the rating files in this bundle.

## Reproducing the headline numbers

Each numbered result in the paper maps to a computation:

| Result | Computation | Inputs |
|---|---|---|
| §5.1 Spearman ρ = −0.077, CI [−0.396, 0.258] | Fisher-z 95% CI on n=36 single-rater agreement pairs | (rating data not in this v1.0 bundle; pending privacy review) |
| §5.3 Cohen's κ (three pairs) | √((1−κ²)/n) approximation | (rating data not in this v1.0 bundle) |
| §6.3 Table 6 (49% → 67% → 84%) | Three-stage cumulative-pipeline holdout pass rate | (holdout case identifiers not in this v1.0 bundle) |
| §6.3(i) latency 22.0s, CI [20.7, 23.4]s | Bootstrap 95% CI on n=23 per-note latency | `em-benchmark-bootstrap-ci.json` (this bundle) |
| §8 Table 5 ablation rates and Wilson CIs | Wilson 95% CI on `failingChecks/totalChecks` per condition | `ablation_results.json` (this bundle) |
| §8 Table 5 per-case pass-rate CIs | Paired bootstrap (10k resamples, seed 42) on `perNotePassCounts` | `ablation_results.json` (this bundle) |
| §8 paired delta B − C, CI [−0.0023, +0.0345] | Same paired bootstrap on the per-case rate difference | `ablation_results.json` (this bundle) |

## Reproducing the bootstrap CIs

The script `scripts/scribe_benchmark/bootstrap_ci.ts` (in the source repository) computes the bootstrap CIs reported in §6.3(i). The ablation per-case CIs and paired-delta CIs reported in §8 are computed by a short Python 3.11 script with seed 42; the script will be added to this directory before peer-review submission.

## Versioning

- **v1.0** (this directory): staged 2026-05-23, contains the three JSON files above plus this README.
- A future **v1.1** (planned for peer-review submission): will add the anonymized pairwise rating files (pending privacy review by Sayvant and the deployment site) and the per-case holdout pass identifiers for Table 6.

## License (pending public release)

When publicly released, this bundle will be made available under the Creative Commons Attribution 4.0 International License (CC BY 4.0). Until then, the contents of this directory are governed by the source repository's access controls.

## Citation

If you use this bundle, please cite the source paper:

> Napier, A., Wiley, J., Heslin, M. *Closed-Loop Quality Assurance for Production Clinical AI Documentation*. arXiv preprint (2026).
