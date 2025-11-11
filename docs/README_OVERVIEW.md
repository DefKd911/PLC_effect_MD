# Project Overview and Workflow Context

This repository documents our effort to predict dynamic strain aging (DSA) and the Portevin–Le Châtelier (PLC) effect in Al–5 wt % Mg using molecular dynamics (MD) and follow-on analyses. It serves three audiences:

1. **New collaborators** – understand the scope, milestones already completed, and what remains.
2. **Recruitment/mentoring** – onboard students by pointing them to focused READMEs for each workflow stage.
3. **Future validation** – provide a traceable record of data sources, scripts, and assumptions.

## High-Level Objectives

1. Generate reliable Mg diffusion coefficients in Al using MD (bulk and interface geometries).
2. Fit Arrhenius relations to extrapolate diffusivity into sub-simulation temperature ranges.
3. Combine diffusivity with mechanistic models (capture radius vs waiting distance) to evaluate DSA/PLC conditions at 300–450 K under a strain rate of 10⁻³ s⁻¹.
4. Document every stage so contributors can reproduce, critique, or extend the work.

## Current Status Snapshot

- **MD Diffusion Data**: Runs completed at 700/850/900 K for the interface system (1 k atoms). Longer runs or larger cells are still needed for Mg R² ≥ 0.95, but provisional diffusivities were extracted.
- **Arrhenius Fit**: Log-space regression now yields \(D_0 \approx 1.23 \times 10^{-5}\) m² s⁻¹ and \(Q \approx 80.5\) kJ mol⁻¹ using the interface interdiffusion coefficients.
- **DSA Assessment**: Updated `analyze_dsa.py` interpolates diffusivity, applies a pipe diffusion factor, and compares diffusion and waiting times for multiple \( \rho_m, L_c, L_t \) combinations. Current data suggests DSA onset around 430–450 K for \( \rho_m = 10^{12} \) m⁻², \( L_c = 1 \) nm, \( L_t = 10 \) µm.
- **Documentation**: This overview links to focused READMEs for each major task (diffusion MD setup, Arrhenius fitting, MSD QA, interface modeling, potentials, DSA theory, and directory structure).

## Workflow Timeline (Stages)

| Stage | Description | Deliverables |
|-------|-------------|--------------|
| 1. System Setup | Build bulk and interface Al–Mg cells, configure MEAM potential | `inputs/`, `potentials/`, `docs/README_INTERFACE_MODEL.md` |
| 2. MD Production | Run LAMMPS scripts for MSD collection at multiple temperatures | `outputs/interface_*`, `docs/README_DIFFUSION_MD.md` |
| 3. MSD QA | Evaluate linearity (R²) and trends; iterate on run length/size | `scripts/check_msd_quality.py`, `docs/README_MSD_QUALITY.md` |
| 4. Diffusivity Extraction | Convert MSD to D, assemble CSV | `outputs/analysis/interface_diffusivity_1k.csv` |
| 5. Arrhenius Fit | Log-space regression + extrapolation | `docs/README_ARRHENIUS.md`, plots in `outputs/analysis/` |
| 6. DSA Modeling | τ_diff vs τ_wait, PLC prediction | `scripts/analyze_dsa.py`, `docs/README_DSA_PLC.md` |
| 7. Reporting & Onboarding | Summaries, QA notes, next steps | `docs/README_PROJECT_STRUCTURE.md`, `README_UPDATED.md` |

## Next Actions

1. **Improve MSD quality** – extend 700 K and 900 K interface runs to ≥ 0.6 ns or build a larger (6×6) cross-section to reduce noise.
2. **Re-fit Arrhenius** with improved diffusivities; update DSA plots accordingly.
3. **Automate QA** – capture R² thresholds and warnings in CI or notebooks.
4. **Integrate experimental comparisons** – add literature lines to MSD/Arrhenius plots for benchmarking.

## How to Use the Documentation

- Start here for context, then dive into the specific READMEs:
  - [`README_DIFFUSION_MD.md`](README_DIFFUSION_MD.md) – running and interpreting LAMMPS diffusion simulations.
  - [`README_INTERFACE_MODEL.md`](README_INTERFACE_MODEL.md) – rationale for the interface setup and MEAM potential mapping.
  - [`README_MSD_QUALITY.md`](README_MSD_QUALITY.md) – MSD diagnostics, R² thresholds, mitigation strategies.
  - [`README_ARRHENIUS.md`](README_ARRHENIUS.md) – Arrhenius fitting, extrapolation, and uncertainty.
  - [`README_DSA_PLC.md`](README_DSA_PLC.md) – mechanistic background and how we used diffusion data for PLC prediction.
  - [`README_PROJECT_STRUCTURE.md`](README_PROJECT_STRUCTURE.md) – directory map and data flow.
  - [`README_POTENTIALS.md`](README_POTENTIALS.md) – provenance and usage tips for MEAM files.

For onboarding or recruitment, point new team members to this overview, then assign them one of the focused READMEs based on their role (simulation, analysis, theory, QA).


