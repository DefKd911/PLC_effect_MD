# MD Study of Dynamic Strain Aging (DSA) in Al-5 wt% Mg

This repository couples molecular dynamics (MD), Arrhenius fitting, and analytical modelling to identify when Mg solutes trigger the Portevin–Le Chatelier (PLC) effect in an Al-5 wt% Mg alloy. The interface-based workflow is now the validated production path. Legacy bulk-diffusion workflows remain documented for reproducibility and future recovery.

---

## Documentation Hub

| Topic | README |
|-------|--------|
| Project overview and status | `docs/README_OVERVIEW.md` |
| Interface MD setup and execution | `docs/README_DIFFUSION_MD.md` |
| Interface geometry and MEAM notes | `docs/README_INTERFACE_MODEL.md` |
| Arrhenius fitting and extrapolation | `docs/README_ARRHENIUS.md` |
| DSA/PLC modelling background | `docs/README_DSA_PLC.md` |
| MSD QA rules and mitigation | `docs/README_MSD_QUALITY.md` |
| Potential provenance and usage | `docs/README_POTENTIALS.md` |
| Directory and file map | `docs/README_PROJECT_STRUCTURE.md` |

Start with the overview, then jump to the README that matches your task (simulation, analysis, QA, or theory).

---

## Current Status and Outputs

- Interface diffusivity table: `outputs/analysis/interface_diffusivity_1k.csv`
- Arrhenius parameters (interdiffusion): `outputs/analysis/arrhenius_interface_interdiff_params.csv`
- DSA scans and plots: `outputs/analysis/dsa_*.csv`, `outputs/analysis/tau_comparison.png`
- MSD trend figures: `outputs/analysis/msd_trend_interface_T700_1k.png`, `...T850_1k.png`, `...T900_1k.png`
- Bulk pathway artefacts (invalid slopes): `outputs/analysis/diffusivity_bulk.csv`

Interface diffusivities (1k-atom cell, approximately 0.1–0.3 ns production):

| T (K) | D_Mg (m^2 s^-1) | R2_Mg | D_Al (m^2 s^-1) | R2_Al | D_interdiff (m^2 s^-1) |
|-------|-----------------|-------|-----------------|-------|-------------------------|
| 700 | 1.09e-11 | 0.79 | 3.06e-12 | 0.92 | 1.05e-11 |
| 850 | 2.15e-10 | 0.91 | 1.09e-09 | 0.99 | 2.64e-10 |
| 900 | 5.58e-11 | 0.45 | 1.85e-09 | 0.99 | 1.55e-10 |

Arrhenius fit (interface interdiffusion, log-space regression):

- D0 = (1.23 ± 0.54) × 10^-5 m^2 s^-1
- Q = (80.5 ± 29.5) kJ mol^-1 (approximately 0.84 eV per atom)
- Fit quality is limited by noisy Mg MSD slopes at 700 K and 900 K (R2 < 0.9).

DSA prediction snapshot (`python scripts\analyze_dsa.py`):

- For rho_m = 1e12 m^-2, L_c = 1 nm, L_t = 10 micrometres, the PLC window lies near 430–450 K (tau_diff / tau_wait between 0.1 and 10).
- Full parameter sweeps and figures reside in `outputs/analysis/dsa_*.csv` and `outputs/analysis/tau_comparison.png`.

`outputs/analysis/summary_report.md` is not generated yet. Run `python scripts\generate_report.py` after MSD fits meet quality thresholds.

---

## Quick Start (Interface Pipeline)

```powershell
pip install -r requirements.txt
python scripts\create_interface_system.py --nx 4 --ny 4 --nz-al 12 --nz-mg 4 --output inputs\interface\interface_system_small.data
lmp -in inputs\interface\in.interface_diffusion -var T 850 -log outputs\interface_1k\log_T850_meam.log
python scripts\analyze_interface_msd.py outputs\interface_1k\msd_interface_T850.dat
python scripts\fit_arrhenius.py --input outputs/analysis/interface_diffusivity_1k.csv --species interdiff --extrapolate
python scripts\analyze_dsa.py
```

- Modify `prod_steps` and cell dimensions before re-running; generate fresh MSD plots via `python scripts\plot_interface_msd.py`.
- Use `python scripts\check_msd_quality.py --pattern outputs\interface_1k\msd_interface_T*.dat` to flag sub-threshold R2.
- `python run_all.py` orchestrates the full workflow once MSD data pass QA.

---

## Next Steps

1. Extend the 700 K and 900 K interface runs to at least 0.6 ns (or adopt a 6x6 cross-section) to push Mg R2 above 0.95.
2. Refit the Arrhenius model with improved slopes and refresh DSA sweeps and plots.
3. Benchmark interface diffusivities against literature values and overlay them in the plotting scripts.
4. Decide whether to rehabilitate or retire the bulk workflow; document the decision in `docs/README_OVERVIEW.md`.
5. Generate `outputs/analysis/summary_report.md` once the refreshed data clear QA.

---

## Repository Layout (abridged)

```
docs/                  # Focused READMEs for each workflow stage
inputs/interface/      # LAMMPS scripts and data for interface MD
inputs/bulk/           # Legacy bulk MD inputs (archived workflow)
outputs/interface_1k/  # Latest MEAM MSD logs and profiles
outputs/analysis/      # Diffusivity tables, Arrhenius fit, DSA scans, plots
scripts/               # Python utilities (setup, QA, fitting, DSA, reporting)
potentials/            # MEAM potential files and usage notes
```

See `docs/README_PROJECT_STRUCTURE.md` for the full directory map.

---

## Legacy Workflows and Previous Approaches

The original plan targeted bulk Al-Mg diffusion using a 6x6x6 (864-atom) cell and three NVT production runs (500, 600, 700 K). Key artefacts remain for traceability even though the workflow currently fails QA:

- Bulk setup and inputs: `scripts/create_bulk_system.py`, `inputs/bulk/in.bulk_diffusion`, `outputs/bulk/`.
- Bulk diffusivity and Arrhenius targets: `outputs/analysis/diffusivity_bulk.csv`, `outputs/analysis/arrhenius_params_bulk.csv` (contain negative diffusivities and R2 << 0.95).
- Analytical framework: `docs/README_ARRHENIUS.md` and `docs/README_DSA_PLC.md` describe how bulk diffusivity feeds pipe-diffusion corrections (D_eff = D_bulk (1 + f_pipe)) and tau_diff versus tau_wait comparisons.
- Professor feedback and scope changes: summarised in `docs/README_OVERVIEW.md`, including reduced temperature coverage, analytical pipe corrections, and the separation of capture radius L_c and travel distance L_t.

These resources should be consulted if the bulk branch is revived; otherwise treat them as historical documentation.

---

## Project Team and License

- Kartik Dua
- Soham Das
- Kashish
- Vishal Ram
- Rishika Shreshth

Academic research use only. Source: https://github.com/DefKd911/PLC_effect_MD.git

Last updated: interface workflow complete; bulk plan archived pending MSD improvements.

---

## Legacy Reference (Bulk-Focused Plan)

> **Context:** The section below preserves the prior README (bulk-focused workflow) so the team can recover historical status, objectives, and instructions. Treat any commands or statuses as archival unless otherwise noted.

### Documentation Map

| Topic | README |
|-------|--------|
| Overall context & milestones | `docs/README_OVERVIEW.md` |
| Running interface diffusion MD | `docs/README_DIFFUSION_MD.md` |
| Interface geometry & MEAM setup | `docs/README_INTERFACE_MODEL.md` |
| Potential provenance & usage | `docs/README_POTENTIALS.md` |
| MSD QA rules & mitigation | `docs/README_MSD_QUALITY.md` |
| Arrhenius regression & extrapolation | `docs/README_ARRHENIUS.md` |
| DSA/PLC theory & results | `docs/README_DSA_PLC.md` |
| Directory/data flow | `docs/README_PROJECT_STRUCTURE.md` |

Start with the overview, then follow the path appropriate for simulation, analysis, or theoretical tasks.

### Current Objectives (Legacy)

1. **Interface MD** – Use an explicit Al\|Mg bilayer (MEAM) to capture asymmetrical interdiffusion. *(Superseded by validated interface workflow above.)*
2. **Diffusivity Extraction** – Convert MSD to D(T), ensuring Mg R² ≥ 0.95 wherever possible.
3. **Arrhenius Fit** – Obtain \(D_0\) and \(Q\) via log-space regression; extrapolate to 300–450 K.
4. **DSA/PLC Prediction** – Compare \( \tau_{\text{diff}} = L_c^2/D_{\text{eff}} \) with \( \tau_{\text{wait}} = L_t/(\rho_m b \dot{\varepsilon}) \) to locate PLC temperature windows at \(10^{-3}\) s⁻¹.

Bulk MD runs are archived; the interface route is the main production path for PLC analysis.

### Workflow Snapshot (Legacy)

1. **Build system** (`create_interface_system.py`)
2. **Run MD** (`inputs/interface/in.interface_diffusion`)
3. **MSD QA & diffusivity** (`analyze_interface_msd.py`, `check_msd_quality.py`)
4. **Arrhenius fit** (`fit_arrhenius.py` – log-space, extrapolation)
5. **DSA analysis** (`analyze_dsa.py` – τ_diff vs τ_wait)
6. **Plots & docs** stored under `outputs/analysis/`

Each stage is documented in the READMEs listed above.

### Legacy Results (1 k-atom interface, ~0.1–0.3 ns production)

**Diffusivity table** (`outputs/analysis/interface_diffusivity_1k.csv`):

| T (K) | D_Mg (m²/s) | R²_Mg | D_Al (m²/s) | R²_Al | D_interdiff (m²/s) |
|-------|-------------|-------|-------------|-------|---------------------|
| 700 | \(1.1\times10^{-11}\) | 0.79 | \(3.1\times10^{-12}\) | 0.92 | \(1.0\times10^{-11}\) |
| 850 | \(2.2\times10^{-10}\) | 0.91 | \(1.1\times10^{-9}\) | 0.99 | \(2.6\times10^{-10}\) |
| 900 | \(5.6\times10^{-11}\) | 0.45 | \(1.9\times10^{-9}\) | 0.99 | \(1.5\times10^{-10}\) |

**Arrhenius (interdiffusion, log-fit)** – `outputs/analysis/arrhenius_interface_interdiff_params.csv`

- \(D_0 = (1.23 \pm 0.54)\times10^{-5}\) m²/s  
- \(Q = (80.5 \pm 29.5)\) kJ/mol (≈ 0.84 eV/atom)  
- R² ≈ 0.88 (limited by Mg R² < 0.95 at 700 K & 900 K)

**DSA prediction** – `outputs/analysis/tau_comparison.png`

- For \( \rho_m = 10^{12} \) m⁻², \( L_c = 1 \) nm, \( L_t = 10 \) µm → PLC regime around **430–450 K** (ratio 0.1–10).  
- CSVs for all \( (\rho_m, L_c, L_t) \) combos are in `outputs/analysis/dsa_*.csv`.

### Limitations & Open Work (Legacy)

1. **Short MSD windows** – 700/900 K runs only ~0.12–0.3 ns ⇒ Mg slopes noisy (R² < 0.95).  
   ➜ Extend to ≥ 0.6 ns or increase lateral size (6×6) to stabilise MSD.
2. **Finite cross-section** – 4×4 cell amplifies fluctuations; evaluate larger systems when feasible.
3. **Pipe diffusion** – Treated analytically (`D_eff = D (1 + f_pipe)`); no explicit dislocation MD yet.
4. **Temperature coverage** – Add 750 K (or 650 K) to strengthen Arrhenius regression once MSD quality improves.
5. **Experimental comparison** – Pending; schedule once revised diffusivities are available.

### Repository Layout (Legacy View)

```
docs/                  # Focused READMEs for each workflow stage
inputs/interface/      # LAMMPS scripts & data for interface diffusion
outputs/interface_1k/  # Latest MSD, logs, profiles
outputs/analysis/      # Diffusivity tables, Arrhenius plots, DSA results
scripts/               # Python helpers (setup, MSD QA, Arrhenius, DSA, plotting)
potentials/            # Mg–Al–Zn MEAM files + instructions
```

Full map: `docs/README_PROJECT_STRUCTURE.md`.

### Quick Start (Legacy Commands)

```powershell
pip install -r requirements.txt
python scripts\create_interface_system.py --nx 4 --ny 4 --nz-al 12 --nz-mg 4
lmp -in inputs\interface\in.interface_diffusion -var T 850 -log outputs\interface_1k\log_T850.log
python scripts\analyze_interface_msd.py outputs\interface_1k\msd_interface_T850.dat
python scripts\fit_arrhenius.py --input outputs/analysis/interface_diffusivity_1k.csv --species interdiff --extrapolate
python scripts\analyze_dsa.py
```

Adapt run length (`prod_steps`) and system size as needed; re-run MSD QA before updating the diffusivity table.

### Next Steps (Legacy)

1. Extend 700 K & 900 K runs to ≥ 0.6 ns (or larger cross-sections) to push Mg R² ≥ 0.95.
2. Add another temperature (e.g., 750 K), refit Arrhenius with R² thresholding.
3. Explore pipe-factor sensitivity (`--pipe-factor` in `analyze_dsa.py`) and compare with literature PLC maps.
4. Update plots/READMEs as improved data arrive; integrate experimental benchmarks.

### Project Team & License (Legacy Listing)

Kartik Dua · Rishika Shresth · Soham Das · Kashish · Vishal Ram · Ashish Chin  
Academic research use only. Source: https://github.com/DefKd911/PLC_effect_MD.git

_Last updated (legacy): incorporating interface-based diffusivity workflow, log-space Arrhenius fit, and PLC prediction._

### Scientific Objectives (Legacy)

#### Project Overview

This project conducts **Molecular Dynamics (MD) simulations** to predict and explain the **Dynamic Strain Aging (DSA)** or **Portevin–Le Chatelier (PLC) effect** in Al–5 wt% Mg alloy. The core deliverable is **MD-derived diffusivity data** (D(T)) validated and used in analytical DSA models.

**Problem Statement:** Predict DSA/PLC effect in Al-5wt%Mg alloy in the temperature range of 300 K, 350 K, 400 K, 450 K, considering strain rate of 10⁻³/s, using the concept of diffusion time of solutes versus waiting time of dislocations.

#### Primary Goal

Calculate diffusivity (D) of Mg in Al using MD, determine activation energy (Q) and pre-exponential factor (D₀), and use these to compare solute diffusion time (τ_diff) and dislocation waiting time (τ_wait) to identify when/if DSA can occur.

#### Five Main Objectives

1. **Compute Mg Diffusion in Bulk Al (D_bulk(T))**
   - Measure D at multiple temperatures using MD
   - Derive D₀ and Q via Arrhenius fit: D = D₀ × exp(-Q/(R×T))
   - Extrapolate to 300-450 K for DSA comparison
2. **Apply Pipe Diffusion Correction (Analytical)**
   - Use analytical factor: D_eff = D_bulk × (1 + f_pipe)
   - No separate dislocation MD simulations needed (per professor feedback)
3. **Use Two Separate Length Scales in DSA Model**
   - **L_c (capture radius):** nm scale, for τ_diff = L_c² / D_eff
   - **L_t (travel distance):** µm scale, for τ_wait = L_t / (ρ_m × b × ε̇)
   - **Critical:** These are DIFFERENT length scales with different physical meanings!
4. **Compute DSA Condition**
   - Compare τ_diff vs τ_wait at 300-450 K
   - Identify temperature window where τ_diff ≈ τ_wait (DSA regime)
5. **Validate with Experimental Data**
   - Compare MD-derived D(T) with literature values
   - Discuss physical reasons for any deviations

#### Updated Workflow (Per Professor Feedback)

| Aspect | Original | Updated (Per Professor) |
|--------|----------|-------------------------|
| **Temperatures** | 5-6 temperatures | **3 temperatures** (500, 600, 700 K) |
| **System size** | 32,000 atoms | **864 atoms** (optimized) |
| **Simulation time** | 10 ns production | **1 ns production** (shorter at higher T) |
| **Dislocation MD** | Separate simulations | **Analytical factor only** |
| **Length scales** | Single L value | **Two L values: L_c and L_t** |
| **Binding energy** | MD calculations | **Literature values** |

#### Complete Workflow Stages (Legacy Status)

- **Stage 1: System Setup** ✅ – Create optimized bulk system, layered interface, validate length scales, verify potential.
- **Stage 2: Bulk Diffusion MD** ⏳ – Runs planned at 500/600/700 K (archived inputs under `inputs/bulk/`).
- **Stage 2B: Interface Diffusion MD** ⏳ – Alternative interface simulations (now superseded by validated workflow above).
- **Stage 3: Extract Diffusivity** ⏳ – Analyze MSD data, require R² > 0.95, save to `outputs/analysis/diffusivity_bulk.csv`.
- **Stage 4: Arrhenius Fit** ⏳ – Fit Arrhenius relation, extrapolate to 300-450 K.
- **Stage 5: Analytical Pipe Diffusion** ⏳ – Apply correction \(D_{\text{eff}} = D_{\text{bulk}} (1 + f_{\text{pipe}})\).
- **Stage 6: DSA Condition Analysis** ⏳ – Compute τ_diff and τ_wait, identify PLC window, store results.
- **Stage 7: Report Generation** ⏳ – Produce plots and markdown summary (pending regenerated data).

#### Project Structure (Legacy)

```
PLC_effect/
├── README.md                    # This file - project overview
├── constants.py                 # Physical constants & parameters
├── requirements.txt             # Python dependencies
├── run_all.py                   # Main workflow script
│
├── potentials/                  # Interatomic potential
│   ├── Al-Mg.eam.fs            # EAM potential (Mendelev et al. 2009)
│   └── README.md               # Potential setup instructions
│
├── inputs/                      # LAMMPS input scripts
│   ├── bulk/                   # Bulk diffusion simulations
│   │   ├── in.bulk_diffusion  # Main input file (updated)
│   │   └── bulk_system.data   # System file (864 atoms)
│   └── interface/             # Al/Mg layered interface simulations
│       ├── in.interface_diffusion
│       └── interface_system.data
│
├── outputs/                     # Simulation results
│   ├── bulk/                   # Bulk diffusion outputs
│   │   ├── msd_T*.dat        # MSD data files
│   │   ├── traj_T*.lammpstrj # Trajectories (optional)
│   │   └── log_T*.log        # LAMMPS logs
│   ├── interface/             # Interface diffusion outputs (optional)
│   │   ├── msd_interface_T*.dat
│   │   ├── profile_*_T*.dat
│   │   └── traj_interface_T*.lammpstrj
│   └── analysis/              # Analysis results
│       ├── diffusivity_bulk.csv
│       ├── arrhenius_params_bulk.csv
│       ├── tau_comparison.png
│       └── summary_report.md
│
├── scripts/                     # Python analysis scripts
│   ├── create_bulk_system.py          # Generate system
│   ├── create_interface_system.py     # Generate layered Al/Mg interface
│   ├── compute_length_scales.py       # Validate L_c and L_t
│   ├── run_bulk_diffusion.py          # Run MD simulations
│   ├── analyze_msd.py                 # Extract diffusivity (Mg & Al species)
│   ├── fit_arrhenius.py               # Fit Arrhenius equation
│   ├── analyze_dsa.py                 # DSA condition analysis
│   ├── plot_results.py                # Generate plots
│   └── generate_report.py             # Final report
│
└── archive/                     # Old/unused files (dislocation, binding)
```

#### Additional Legacy Notes

- **Key Physical Parameters:** Composition, Burgers vector, strain rate, dislocation densities, temperature ranges, L_c/L_t scales, simulation parameters.
- **Key Features:** Emphasis on two distinct length scales, analytical pipe diffusion correction, optimized workflow parameters.
- **Expected Deliverables:** `diffusivity_bulk.csv`, `arrhenius_params_bulk.csv`, `dsa_*.csv`, `arrhenius_fit.png`, `tau_comparison.png`, and `summary_report.md` (pending regeneration).
- **Documentation Files:** `START_HERE.md`, `STEP_BY_STEP_GUIDE.md`, `QUICK_COMMANDS.md`, `UPDATED_WORKFLOW.md`, `PROFESSOR_ADVICE.md`, `MSD_ANALYSIS.md`, `PS_VERIFICATION.md`.
- **Technical Details:** MD setup (EAM/FS potential, NPT→NVT ensemble, Nosé–Hoover thermostat), validation metrics, DSA condition equations.
- **Scientific Background:** Rationale for MD-derived diffusivity, importance of pipe diffusion, distinct length scales, previously corrected mistakes.
- **Execution Timeline (Legacy):** Setup complete; diffusion and analysis stages pending; total estimated duration 4–7 hours (see table in legacy docs).
- **Usage Examples & Troubleshooting:** Commands for running simulations, analyzing MSD/Arrhenius/DSA, generating reports, and resolving common issues.
- **References & Support:** Potential references, LAMMPS documentation, quick-start guides.

---

