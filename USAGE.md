# Usage Guide

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Place potential file:**
   - Download or obtain an EAM potential for Al-Mg
   - Place it in `potentials/EAM_AlMg.eam.alloy`
   - See `potentials/README.md` for more information

3. **Run complete workflow:**
   ```bash
   python run_all.py
   ```

## Step-by-Step Usage

### Step 1: Create Simulation Systems

```bash
# Create bulk system
python scripts/create_bulk_system.py

# Create dislocation system
python scripts/create_dislocation_system.py
```

### Step 2: Run MD Simulations

**Option A: Using provided scripts (requires LAMMPS in PATH)**

```bash
# Run bulk diffusion at multiple temperatures
python scripts/run_bulk_diffusion.py
```

**Option B: Manual LAMMPS execution**

```bash
# For each temperature, run:
lmp -in inputs/bulk/in.bulk_T600.lmp -log outputs/bulk/log_T600.log
lmp -in inputs/bulk/in.bulk_T700.lmp -log outputs/bulk/log_T700.log
# ... etc
```

### Step 3: Analyze Results

```bash
# Analyze MSD data and extract diffusivity
python scripts/analyze_msd.py

# Fit Arrhenius equation
python scripts/fit_arrhenius.py

# Analyze dislocation diffusion (if available)
python scripts/analyze_dislocation_diffusion.py

# Compute binding energy (if available)
python scripts/compute_binding_energy.py
```

### Step 4: DSA Analysis

```bash
# Analyze DSA conditions
python scripts/analyze_dsa.py
```

### Step 5: Generate Plots and Report

```bash
# Generate all plots
python scripts/plot_results.py

# Generate final report
python scripts/generate_report.py
```

## Output Files

All results are saved in `outputs/analysis/`:

- `diffusivity_bulk.csv` - Bulk diffusivity data
- `diffusivity_core.csv` - Core diffusivity data
- `binding_energy.csv` - Binding energy data
- `capture_radius.csv` - Capture radius data
- `arrhenius_params_bulk.csv` - Arrhenius fit parameters
- `tau_comparison.png` - DSA condition plots
- `arrhenius_fit.png` - Arrhenius fit plot
- `eb_vs_r.png` - Binding energy plot
- `summary_report.md` - Final summary report

## Customization

### Change Temperature Range

Edit `constants.py`:
```python
T_md = [600, 700, 800, 900, 1000, 1100]  # MD simulation temperatures
T_dsa = np.linspace(300, 450, 16)  # DSA analysis temperatures
```

### Change Dislocation Density

Edit `constants.py`:
```python
rho_m_values = [1e12, 1e13, 1e14]  # m⁻²
```

### Change Potential File

Edit LAMMPS input files or modify the `pot_file` variable in scripts.

## Troubleshooting

### LAMMPS not found

- Ensure LAMMPS is installed and `lmp` is in your PATH
- Or use full path: `/path/to/lammps/src/lmp_serial -in input.lmp`

### Missing data files

- Run simulations first to generate MSD data files
- Check that output directories exist and are writable

### Import errors

- Ensure all Python dependencies are installed: `pip install -r requirements.txt`
- Check that you're running scripts from the project root directory

### Low R² values in MSD fits

- Increase simulation time (edit `production_time` in `constants.py`)
- Check that system is properly equilibrated
- Verify potential file is appropriate for Al-Mg system

## Validation

Run validation checks:
```bash
python scripts/validate_simulation.py
```

This checks:
- MSD linearity (R² > 0.95)
- Temperature stability
- Energy drift

## Jupyter Notebooks

For interactive analysis, use the template notebook:
```bash
jupyter notebook notebooks/analysis_template.ipynb
```


