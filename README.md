# MD Study of Dynamic Strain Aging (DSA) in Al-5wt%Mg Alloy

## Project Overview

This project conducts Molecular Dynamics (MD) simulations to predict and explain the Dynamic Strain Aging (DSA) or Portevin–Le Chatelier (PLC) effect in Al–5 wt% Mg alloy.

## Objectives

1. **Compute Mg Diffusion in Bulk Al** - Measure D_bulk(T) using MD and derive D₀ and Q via Arrhenius fit
2. **Compute Diffusion Near Dislocation Core** - Quantify enhanced pipe diffusion (D_core(T))
3. **Compute Mg–Dislocation Binding Energy** - Determine capture distance L = r_c
4. **DSA Condition Analysis** - Predict DSA feasibility using τ_diff ≈ τ_wait
5. **Validation** - Compare MD results with experimental data

## Project Structure

```
PLC_effect/
├── potentials/          # Interatomic potential files
├── inputs/             # LAMMPS input scripts
│   ├── bulk/          # Bulk diffusion simulations
│   ├── dislocation/   # Dislocation core diffusion
│   └── binding/       # Binding energy calculations
├── outputs/           # Simulation results
│   ├── bulk/         # Bulk diffusion outputs
│   ├── dislocation/  # Dislocation outputs
│   ├── binding/      # Binding energy outputs
│   └── analysis/     # Analysis results and plots
├── scripts/           # Python analysis scripts
└── notebooks/         # Jupyter notebooks for analysis
```

## Physical Constants

- Burgers vector: b = 2.86 × 10⁻¹⁰ m
- Strain rate: ε̇ = 10⁻³ s⁻¹
- Mobile dislocation density: ρ_m = [10¹², 10¹³, 10¹⁴] m⁻²
- Temperature range: 600-1100 K (MD), 300-450 K (extrapolation for DSA)

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place interatomic potential file:**
   - Download EAM potential for Al-Mg
   - Place in `potentials/EAM_AlMg.eam.alloy`

3. **Run complete workflow:**
   ```bash
   python run_all.py
   ```

See `QUICK_START.md` for detailed instructions and `USAGE.md` for comprehensive usage guide.

## Usage

### Automated Workflow
```bash
python run_all.py
```

### Step-by-Step
1. Create systems: `python scripts/create_bulk_system.py`
2. Run simulations: `python scripts/run_bulk_diffusion.py` (or run LAMMPS manually)
3. Analyze MSD: `python scripts/analyze_msd.py`
4. Fit Arrhenius: `python scripts/fit_arrhenius.py`
5. DSA analysis: `python scripts/analyze_dsa.py`
6. Generate report: `python scripts/generate_report.py`

## Requirements

- LAMMPS (with Python interface)
- Python 3.8+
- NumPy, SciPy, Matplotlib, Pandas
- OVITO (optional, for visualization)

