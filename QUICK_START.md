# Quick Start Guide

## Prerequisites

1. **Python 3.8+** with packages:
   ```bash
   pip install numpy scipy pandas matplotlib
   ```

2. **LAMMPS** installed and accessible via `lmp` command
   - Download from: https://www.lammps.org/
   - Or use conda: `conda install -c conda-forge lammps`

3. **EAM Potential** for Al-Mg
   - Place in `potentials/EAM_AlMg.eam.alloy`
   - See `potentials/README.md` for sources

## 5-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create simulation systems
python scripts/create_bulk_system.py

# 3. Run one test simulation (if LAMMPS available)
# Edit inputs/bulk/in.bulk_diffusion to set T=800
# Then run: lmp -in inputs/bulk/in.bulk_diffusion -log outputs/bulk/log_T800.log

# 4. Analyze results (if you have MSD data)
python scripts/analyze_msd.py
python scripts/fit_arrhenius.py

# 5. Generate report
python scripts/generate_report.py
```

## Complete Workflow

For the full automated workflow:

```bash
python run_all.py
```

This will:
1. Create all simulation systems
2. Prompt to run LAMMPS simulations
3. Analyze all results
4. Generate plots and final report

## Expected Outputs

After running simulations and analysis, you should have:

- `outputs/analysis/diffusivity_bulk.csv` - Bulk diffusivity at each temperature
- `outputs/analysis/arrhenius_params_bulk.csv` - D₀ and Q values
- `outputs/analysis/arrhenius_fit.png` - Arrhenius plot
- `outputs/analysis/summary_report.md` - Comprehensive report

## Key Results to Check

1. **Activation Energy Q**: Should be ~80-100 kJ/mol for Al-Mg (not 130 kJ/mol)
2. **MSD R²**: Should be > 0.95 for valid fits
3. **DSA Regime**: Check `outputs/analysis/tau_comparison.png` to see where τ_diff ≈ τ_wait

## Troubleshooting

**"LAMMPS not found"**
- Add LAMMPS to PATH, or use full path in scripts
- Or run LAMMPS manually and use analysis scripts only

**"No data files found"**
- Run simulations first to generate MSD data
- Or use provided example data if available

**"Import errors"**
- Run: `pip install -r requirements.txt`
- Ensure you're in project root directory

## Next Steps

1. Review `outputs/analysis/summary_report.md`
2. Check plots in `outputs/analysis/`
3. Compare MD results with experimental literature
4. Adjust parameters in `constants.py` if needed
5. Run additional simulations for different conditions

## Scientific Validation

Before trusting results, verify:

- ✅ Lattice constant matches experimental value (~4.05 Å)
- ✅ MSD shows linear behavior (R² > 0.95)
- ✅ Temperature is stable during NVT runs
- ✅ Activation energy is physically reasonable (~80-100 kJ/mol for Al-Mg)

Run validation:
```bash
python scripts/validate_simulation.py
```


