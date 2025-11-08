# Updated Project Structure (Post-Cleanup)

## ✅ Active Directories

```
PLC_effect/
├── constants.py              # Updated: 3 temps, two L values
├── inputs/
│   └── bulk/                # Only bulk diffusion needed
│       ├── in.bulk_diffusion
│       └── bulk_system.data
├── outputs/
│   ├── bulk/                # Bulk diffusion results
│   └── analysis/            # Analysis results
├── scripts/
│   ├── create_bulk_system.py
│   ├── run_bulk_diffusion.py
│   ├── analyze_msd.py
│   ├── fit_arrhenius.py
│   ├── analyze_dsa.py       # UPDATED: Two L values
│   ├── compute_length_scales.py  # NEW: Validates L_c and L_t
│   ├── plot_results.py
│   └── generate_report.py
└── archive/                 # Old/unused files
    ├── dislocation/
    ├── binding/
    └── [old scripts]
```

## 🎯 Key Features

### Two Different Length Scales (L_c and L_t)

**L_c (Capture Radius):**
- Scale: **nanometers** (1-5 nm)
- Used in: `tau_diff = L_c² / D_eff`
- Physical meaning: Distance for solute capture

**L_t (Travel Distance):**
- Scale: **micrometers** (0.1-10 µm)
- Used in: `tau_wait = L_t / (ρ_m × b × ε̇)`
- Physical meaning: Dislocation travel distance

**CRITICAL:** These are DIFFERENT scales with different meanings!

### Simplified Workflow

1. **Bulk diffusion MD** at 3 temperatures (500, 600, 700 K)
2. **Arrhenius fit** → D₀, Q
3. **Analytical pipe diffusion** → D_eff = D_bulk × (1 + f_pipe)
4. **DSA analysis** with two L values

## 🚀 Quick Start

```bash
# Validate length scales
python scripts/compute_length_scales.py

# Run bulk diffusion at 3 temperatures
python scripts/run_bulk_diffusion.py

# Analyze results
python scripts/analyze_msd.py
python scripts/fit_arrhenius.py
python scripts/analyze_dsa.py
```

## 📋 What Was Removed

- ❌ Dislocation MD simulations
- ❌ Binding energy calculations
- ❌ Extra temperature points (reduced to 3)
- ❌ Long simulation times (reduced to 5 ns)

All moved to `archive/` directory for reference.

