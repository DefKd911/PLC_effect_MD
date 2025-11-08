# Quick Command Reference

## All Commands in One Place

### Setup Verification
```bash
python scripts/compute_length_scales.py
```

### Run Simulations (Choose One)

**Option A: Sequential (one at a time)**
```bash
lmp -in inputs/bulk/in.bulk_diffusion -var T 500 -log outputs/bulk/log_T500.log
lmp -in inputs/bulk/in.bulk_diffusion -var T 600 -log outputs/bulk/log_T600.log
lmp -in inputs/bulk/in.bulk_diffusion -var T 700 -log outputs/bulk/log_T700.log
```

**Option B: Parallel (if you have 3 terminals/CPUs)**
```bash
# Terminal 1
lmp -in inputs/bulk/in.bulk_diffusion -var T 500 -log outputs/bulk/log_T500.log

# Terminal 2
lmp -in inputs/bulk/in.bulk_diffusion -var T 600 -log outputs/bulk/log_T600.log

# Terminal 3
lmp -in inputs/bulk/in.bulk_diffusion -var T 700 -log outputs/bulk/log_T700.log
```

### Analysis Pipeline
```bash
# Step 1: Extract diffusivity from MSD
python scripts/analyze_msd.py

# Step 2: Fit Arrhenius equation
python scripts/fit_arrhenius.py

# Step 3: DSA analysis
python scripts/analyze_dsa.py

# Step 4: Generate plots
python scripts/plot_results.py

# Step 5: Generate report
python scripts/generate_report.py
```

### Check Results
```bash
# Check MSD files exist
ls outputs/bulk/msd_T*.dat

# View diffusivity results
cat outputs/analysis/diffusivity_bulk.csv

# View Arrhenius parameters
cat outputs/analysis/arrhenius_params_bulk.csv

# View final report
cat outputs/analysis/summary_report.md
```

