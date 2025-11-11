# MD Study of Dynamic Strain Aging (DSA) in Al–5 wt % Mg

This repository combines molecular dynamics (MD), Arrhenius fitting, and analytical models to predict when Mg solutes in Al trigger the Portevin–Le Châtelier (PLC) effect. The documentation is split into focused READMEs so each contributor can dive directly into their part of the workflow.

---

## 📚 Documentation Map

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

---

## 🎯 Current Objectives

1. **Interface MD** – Use an explicit Al\|Mg bilayer (MEAM) to capture asymmetrical interdiffusion.
2. **Diffusivity Extraction** – Convert MSD to D(T), ensuring Mg R² ≥ 0.95 wherever possible.
3. **Arrhenius Fit** – Obtain \(D_0\) and \(Q\) via log-space regression; extrapolate to 300–450 K.
4. **DSA/PLC Prediction** – Compare \( \tau_{\text{diff}} = L_c^2/D_{\text{eff}} \) with \( \tau_{\text{wait}} = L_t/(\rho_m b \dot{\varepsilon}) \) to locate PLC temperature windows at \(10^{-3}\) s⁻¹.

Bulk MD runs are archived; the interface route is the main production path for PLC analysis.

---

## 🔄 Workflow Snapshot

1. **Build system** (`create_interface_system.py`)
2. **Run MD** (`inputs/interface/in.interface_diffusion`)
3. **MSD QA & diffusivity** (`analyze_interface_msd.py`, `check_msd_quality.py`)
4. **Arrhenius fit** (`fit_arrhenius.py` – log-space, extrapolation)
5. **DSA analysis** (`analyze_dsa.py` – τ_diff vs τ_wait)
6. **Plots & docs** stored under `outputs/analysis/`

Each stage is documented in the READMEs listed above.

---

## ✅ Current Results (1 k-atom interface, ~0.1–0.3 ns production)

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

---

## ⚠️ Limitations & Open Work

1. **Short MSD windows** – 700/900 K runs only ~0.12–0.3 ns ⇒ Mg slopes noisy (R² < 0.95).  
   ➜ Extend to ≥ 0.6 ns or increase lateral size (6×6) to stabilise MSD.

2. **Finite cross-section** – 4×4 cell amplifies fluctuations; evaluate larger systems when feasible.

3. **Pipe diffusion** – Treated analytically (`D_eff = D (1 + f_pipe)`); no explicit dislocation MD yet.

4. **Temperature coverage** – Add 750 K (or 650 K) to strengthen Arrhenius regression once MSD quality improves.

5. **Experimental comparison** – Pending; schedule once revised diffusivities are available.

All mitigation ideas are captured in `docs/README_MSD_QUALITY.md` and `docs/README_DSA_PLC.md`.

---

## 🗂️ Repository Layout (abridged)

```
docs/                  # Focused READMEs for each workflow stage
inputs/interface/      # LAMMPS scripts & data for interface diffusion
outputs/interface_1k/  # Latest MSD, logs, profiles
outputs/analysis/      # Diffusivity tables, Arrhenius plots, DSA results
scripts/               # Python helpers (setup, MSD QA, Arrhenius, DSA, plotting)
potentials/            # Mg–Al–Zn MEAM files + instructions
```

Full map: `docs/README_PROJECT_STRUCTURE.md`.

---

## 🚀 Quick Start

```powershell
pip install -r requirements.txt
python scripts\create_interface_system.py --nx 4 --ny 4 --nz-al 12 --nz-mg 4
lmp -in inputs\interface\in.interface_diffusion -var T 850 -log outputs\interface_1k\log_T850.log
python scripts\analyze_interface_msd.py outputs\interface_1k\msd_interface_T850.dat
python scripts\fit_arrhenius.py --input outputs/analysis/interface_diffusivity_1k.csv --species interdiff --extrapolate
python scripts\analyze_dsa.py
```

Adapt run length (`prod_steps`) and system size as needed; re-run MSD QA before updating the diffusivity table.

---

## 🔄 Next Steps

1. Extend 700 K & 900 K runs to ≥ 0.6 ns (or larger cross-sections) to push Mg R² ≥ 0.95.
2. Add another temperature (e.g., 750 K), refit Arrhenius with R² thresholding.
3. Explore pipe-factor sensitivity (`--pipe-factor` in `analyze_dsa.py`) and compare with literature PLC maps.
4. Update plots/READMEs as improved data arrive; integrate experimental benchmarks.

---

## 🧑‍🤝‍🧑 Team & License

Kartik Dua · Rishika Shresth · Soham Das · Kashish · Vishal Ram · Ashish Chin  
Academic research use only. Source: https://github.com/DefKd911/PLC_effect_MD.git

_Last updated: incorporating interface-based diffusivity workflow, log-space Arrhenius fit, and PLC prediction._
# MD Study of Dynamic Strain Aging (DSA) in Al-5wt%Mg Alloy

## 📋 Project Overview

This project conducts **Molecular Dynamics (MD) simulations** to predict and explain the **Dynamic Strain Aging (DSA)** or **Portevin–Le Chatelier (PLC) effect** in Al–5 wt% Mg alloy. The core deliverable is **MD-derived diffusivity data** (D(T)) validated and used in analytical DSA models.

**Problem Statement:** Predict DSA/PLC effect in Al-5wt%Mg alloy in the temperature range of 300 K, 350 K, 400 K, 450 K, considering strain rate of 10⁻³/s, using the concept of diffusion time of solutes versus waiting time of dislocations.

---

## 🎯 Scientific Objectives

### Primary Goal
Calculate diffusivity (D) of Mg in Al using MD, determine activation energy (Q) and pre-exponential factor (D₀), and use these to compare solute diffusion time (τ_diff) and dislocation waiting time (τ_wait) to identify when/if DSA can occur.

### Five Main Objectives

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

---

## 🔬 Updated Workflow (Per Professor Feedback)

### Key Changes from Original Plan

| Aspect | Original | Updated (Per Professor) |
|--------|----------|-------------------------|
| **Temperatures** | 5-6 temperatures | **3 temperatures** (500, 600, 700 K) |
| **System size** | 32,000 atoms | **864 atoms** (optimized) |
| **Simulation time** | 10 ns production | **1 ns production** (shorter at higher T) |
| **Dislocation MD** | Separate simulations | **Analytical factor only** |
| **Length scales** | Single L value | **Two L values: L_c and L_t** |
| **Binding energy** | MD calculations | **Literature values** |

### Complete Workflow Stages

#### **Stage 1: System Setup** ✅
- Create optimized Al-5wt%Mg bulk system (6×6×6 = 864 atoms, random Mg distribution)
- Create Al/Mg layered interface system (Al substrate + Mg overlayer)
- Validate length scales (L_c and L_t)
- Verify potential file (Al-Mg.eam.fs)

#### **Stage 2: Bulk Diffusion MD Simulations** ⏳
- Run MD at **3 temperatures:** 500 K, 600 K, 700 K
- Each simulation: 0.1 ns equilibration + 1 ns production (extend if MSD not linear)
- Collect MSD data for Mg and Al atoms separately
- **Time per simulation:** ~1-2 hours
- **Total time:** ~3-6 hours (can run in parallel)

#### **Stage 2B (Optional): Interface Diffusion MD Simulations** ⏳
- Build Mg-over-Al layered system following Fan et al. methodology
- Run MD at selected temperatures (e.g., 600-800 K) to observe Mg penetration
- Output species-specific MSD and concentration profiles (z-direction bins)
- Use to validate alternative diffusivity extraction paths or interdiffusivity

#### **Stage 3: Extract Diffusivity** ⏳
- Analyze MSD data → extract D(T) for Mg (and Al) at each temperature
- Validate MSD linearity (R² > 0.95)
- Save: `outputs/analysis/diffusivity_bulk.csv`

#### **Stage 4: Arrhenius Fit** ⏳
- Fit: D = D₀ × exp(-Q/(R×T))
- Extract D₀ and Q (activation energy)
- Extrapolate to 300-450 K for DSA analysis
- Save: `outputs/analysis/arrhenius_params_bulk.csv`

#### **Stage 5: Analytical Pipe Diffusion** ⏳
- Apply correction: D_eff = D_bulk × (1 + f_pipe)
- f_pipe = 1.0 (default, can vary 0.1-10 for sensitivity)

#### **Stage 6: DSA Condition Analysis** ⏳
- Compute τ_diff = L_c² / D_eff (using L_c: 1-5 nm)
- Compute τ_wait = L_t / (ρ_m × b × ε̇) (using L_t: 0.1-10 µm)
- Compare at 300-450 K
- Identify DSA regime (where τ_diff ≈ τ_wait)
- Save: `outputs/analysis/dsa_*.csv` and plots

#### **Stage 7: Report Generation** ⏳
- Generate Arrhenius plots
- Create τ_diff vs τ_wait comparison plots
- Generate comprehensive markdown report
- Save: `outputs/analysis/summary_report.md`

---

## 📁 Project Structure

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

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with: `numpy`, `scipy`, `pandas`, `matplotlib`
- **LAMMPS** installed and accessible via `lmp` command
- **EAM potential** file: `potentials/Al-Mg.eam.fs` (already included)

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Verify potential file exists
ls potentials/Al-Mg.eam.fs
```

### Execution (5 Steps)

**Step 1: Verify Setup (2 min)**
```bash
python scripts/compute_length_scales.py
python scripts/create_interface_system.py  # Generates layered Al/Mg data file
```

**Step 2: Run Simulations (3-6 hours)**
```bash
# Sequential (one at a time)
lmp -in inputs/bulk/in.bulk_diffusion -var T 500 -log outputs/bulk/log_T500.log
lmp -in inputs/bulk/in.bulk_diffusion -var T 600 -log outputs/bulk/log_T600.log
lmp -in inputs/bulk/in.bulk_diffusion -var T 700 -log outputs/bulk/log_T700.log

# Optional: Interface diffusion (adjust prod_steps inside input as needed)
lmp -in inputs/interface/in.interface_diffusion -var T 700 -log outputs/interface/log_T700.log

# Or parallel (if you have 3 CPU cores)
# Run each in separate terminal
```

**Step 3: Analyze MSD Data (1 min)**
```bash
python scripts/analyze_msd.py
```

**Step 4: Fit Arrhenius (1 min)**
```bash
python scripts/fit_arrhenius.py
```

**Step 5: DSA Analysis & Report (2 min)**
```bash
python scripts/analyze_dsa.py
python scripts/plot_results.py
python scripts/generate_report.py
```

**Or use automated workflow:**
```bash
python run_all.py
```

---

## 📊 Key Physical Parameters

### Material Properties
- **Composition:** Al-5wt%Mg (5.52 at% Mg)
- **Burgers vector:** b = 2.86 × 10⁻¹⁰ m
- **Strain rate:** ε̇ = 10⁻³ s⁻¹
- **Mobile dislocation density:** ρ_m = [10¹², 10¹³, 10¹⁴] m⁻²

### Temperature Ranges
- **MD simulations:** 500, 600, 700 K (3 temperatures, below Al melting ~933 K)
- **DSA analysis:** 300-450 K (extrapolated from Arrhenius fit)

### Length Scales (CRITICAL - Two Different Values!)
- **L_c (capture radius):** 1, 2, 5 nm (for τ_diff calculation)
- **L_t (travel distance):** 0.1, 1.0, 10.0 µm (for τ_wait calculation)
- **Note:** L_c << L_t (typically 100-1000× smaller)

### Simulation Parameters
- **System size:** 864 atoms (6×6×6 unit cells)
- **Equilibration:** 0.1 ns (100,000 steps)
- **Production:** 1 ns (100,000 steps)
- **Timestep:** 1 fs (0.001 ps in LAMMPS)

---

## 🔑 Key Features

### Two Separate Length Scales
This was a critical correction from the professor:
- **L_c (capture radius):** Used in τ_diff = L_c² / D_eff
  - Physical meaning: Distance for solute capture by dislocation
  - Scale: nanometers (1-5 nm)
  
- **L_t (travel distance):** Used in τ_wait = L_t / (ρ_m × b × ε̇)
  - Physical meaning: Distance dislocation travels before pinning
  - Scale: micrometers (0.1-10 µm)

**These are NOT the same!** They have different physical meanings and are used in different equations.

### Analytical Pipe Diffusion
- No separate dislocation MD simulations needed
- Use analytical correction: D_eff = D_bulk × (1 + f_pipe)
- f_pipe = 1.0 (default, can vary for sensitivity)

### Optimized Workflow
- **3 temperatures only** (sufficient for Arrhenius fit)
- **Smaller system** (864 atoms, optimized for speed)
- **Shorter simulations** (1 ns at higher T, acceptable per professor)

---

## 📈 Expected Deliverables

### Data Files
- `diffusivity_bulk.csv` - D(T) at 500, 600, 700 K
- `arrhenius_params_bulk.csv` - D₀ and Q values
- `diffusivity_bulk_extrapolated.csv` - D(T) at 300-450 K
- `dsa_*.csv` - τ_diff vs τ_wait for each parameter combination

### Plots
- `arrhenius_fit.png` - Arrhenius plot (ln D vs 1/T)
- `tau_comparison.png` - DSA condition plot (τ_diff vs τ_wait)

### Report
- `summary_report.md` - Comprehensive project report with:
  - MD-derived D₀ and Q
  - Pipe diffusion enhancement factor
  - DSA temperature window identification
  - Comparison with experimental data

---

## 📚 Documentation Files

- **`START_HERE.md`** - Quick start guide
- **`STEP_BY_STEP_GUIDE.md`** - Detailed execution instructions
- **`QUICK_COMMANDS.md`** - All commands in one place
- **`UPDATED_WORKFLOW.md`** - Complete workflow description
- **`PROFESSOR_ADVICE.md`** - Implementation of professor's feedback
- **`MSD_ANALYSIS.md`** - MSD data quality guidelines
- **`PS_VERIFICATION.md`** - Problem statement compliance check

---

## ⚙️ Technical Details

### MD Simulation Setup
- **Potential:** EAM/FS (Finnis-Sinclair)
- **Ensemble:** NPT (equilibration) → NVT (production)
- **Thermostat:** Nosé–Hoover
- **MSD calculation:** Reset after equilibration for accurate diffusion

### Validation Metrics
- **MSD linearity:** R² > 0.95 required
- **Temperature stability:** ±20 K during NVT
- **Energy drift:** < 0.01 eV/atom/ns

### DSA Condition
DSA occurs when:
```
τ_diff ≈ τ_wait

Where:
τ_diff = L_c² / D_eff        (diffusion time)
τ_wait = L_t / (ρ_m × b × ε̇)  (waiting time)
```

DSA regime: 0.1 < τ_diff / τ_wait < 10

---

## 🎓 Scientific Background

### Why This Matters
- **Literature values are approximate** - Professor wants MD-derived D
- **Pipe diffusion is crucial** - Enhanced diffusion near dislocations affects DSA
- **Two L values are critical** - Capture radius ≠ travel distance (key correction!)

### Previous Mistakes (Now Corrected)
- ❌ Used overly high activation energy (130 kJ/mol) → ✅ Now using MD-derived Q (~80-100 kJ/mol)
- ❌ Used too low dislocation density → ✅ Now exploring 10¹²-10¹⁴ m⁻²
- ❌ Used single L value → ✅ Now using two separate L values (L_c and L_t)
- ❌ Used literature D → ✅ Now computing D from MD

---

## 🔄 Execution Timeline

| Stage | Task | Duration | Status |
|-------|------|----------|--------|
| 1 | Setup & validation | 5 min | ✅ Complete |
| 2 | MD at 500 K | 1-2 hrs | ⏳ Running |
| 2 | MD at 600 K | 1-2 hrs | ⏳ Pending |
| 2 | MD at 700 K | 1-2 hrs | ⏳ Pending |
| 3 | MSD analysis | 1 min | ⏳ Pending |
| 4 | Arrhenius fit | 1 min | ⏳ Pending |
| 5 | DSA analysis | 1 min | ⏳ Pending |
| 6 | Report generation | 1 min | ⏳ Pending |
| **Total** | | **~4-7 hours** | |

---

## 📝 Usage Examples

### Run Single Simulation
```bash
lmp -in inputs/bulk/in.bulk_diffusion -var T 600 -log outputs/bulk/log_T600.log
```

### Analyze Existing Data
```bash
python scripts/analyze_msd.py
python scripts/fit_arrhenius.py
python scripts/analyze_dsa.py
```

### Generate Report
```bash
python scripts/generate_report.py
cat outputs/analysis/summary_report.md
```

---

## 🐛 Troubleshooting

### MSD Not Growing Linearly
- **Check:** Simulation completed full 1 ns
- **Check:** MSD reset after equilibration (fix applied)
- **Solution:** Run at higher T (700 K) first for validation

### Import Errors
```bash
pip install -r requirements.txt
```

### LAMMPS Not Found
- Ensure LAMMPS is installed and `lmp` is in PATH
- Or use full path: `/path/to/lammps/src/lmp_serial -in input.lmp`

### Low R² Values
- Increase simulation time if needed
- Check temperature is stable
- Verify potential file is appropriate

---

## 📖 References

- **Potential:** Mendelev et al. (2009), Phil. Mag. 89, 3269-3285
- **NIST Repository:** https://www.ctcms.nist.gov/potentials/system/Al-Mg/
- **LAMMPS Documentation:** https://docs.lammps.org/

---

## 👥 Project Team

- Kartik Dua
- Rishika Shresth
- Soham Das
- Kashish
- Vishal Ram
- Ashish Chin

---

## 📄 License

This project is for academic research purposes.

---

## 🔗 Repository

**GitHub:** https://github.com/DefKd911/PLC_effect_MD.git

---

## ✅ Current Status

- ✅ Project structure created
- ✅ All scripts developed
- ✅ System optimized (864 atoms)
- ✅ Length scales validated (L_c and L_t)
- ⏳ MD simulations in progress (T500 running)
- ⏳ Analysis pending (waiting for simulation completion)

**Next:** Complete simulations at 3 temperatures, then proceed with analysis pipeline.

---

## 📞 Support

For detailed instructions, see:
- `STEP_BY_STEP_GUIDE.md` - Complete step-by-step guide
- `QUICK_COMMANDS.md` - Quick command reference
- `START_HERE.md` - Quick start overview

---

**Last Updated:** Based on professor feedback - optimized workflow with 3 temperatures, analytical pipe diffusion, and two separate length scales.
