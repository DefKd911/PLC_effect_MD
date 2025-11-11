# Diffusion Simulations with LAMMPS

This document explains how we generate Mg diffusivity data in Al using LAMMPS, with emphasis on the interface geometry that feeds our DSA/PLC analysis.

---

## Objectives

1. Build Al|Mg bilayer cells that mimic the interface studied by Fan et al. (Physica B 715, 2025).
2. Run NPT → NVT MD in the 650–900 K range to capture MSD growth.
3. Export per-species MSD data for downstream Arrhenius fitting.
4. Quantify limitations (run length, cell size) to guide future simulations.

---

## Key Files

| Path | Purpose |
|------|---------|
| `scripts/create_interface_system.py` | Generates Al|Mg layered LAMMPS data files with configurable nx, ny, nz. |
| `inputs/interface/in.interface_diffusion` | Production LAMMPS input invoking MEAM, fixed layers, MSD output. |
| `potentials/MgAlZn.{library,parameter}.meam` | Dickel et al. (2018) MEAM files supporting Al/Mg/Zn interactions. |
| `outputs/interface_1k/msd_interface_T*.dat` | MSD results for the 1 k-atom interface runs. |
| `scripts/check_msd_quality.py` | QA utility for verifying MSD linearity and R². |

---

## System Preparation

1. **Create a data file** (current default: 4×4×(12 Al + 4 Mg) → 1 024 atoms):
   ```powershell
   cd "D:\PLC_effect - Copy"
   python scripts\create_interface_system.py --nx 4 --ny 4 --nz-al 12 --nz-mg 4 ^
       --output inputs\interface\interface_system_small.data
   ```
2. **Potential placement**: Put `MgAlZn.library.meam` and `MgAlZn.parameter.meam` in `potentials/`.
3. **Verify potential**: Run the minimization sanity test (`inputs/interface/test_meam_minimize.in`) to confirm MEAM loads correctly.

---

## Running the Simulations

### Input Overview (`in.interface_diffusion`)

- **Fixed layers**: top/bottom 5 Å atoms have forces set to zero (`setforce 0 0 0`).
- **Thermostats**: only the mobile group is coupled to NPT/NVT; fixed layers maintain cell integrity.
- **Production length**: currently 0.4 ns (400 000 steps). Extend to 0.6–1.0 ns for cleaner Mg MSD.
- **Outputs**:
  - MSD files (per species, x/y/z/total).
  - Number-density profiles for Mg and all atoms.
  - Trajectory dumps for snapshot extraction.

### Example Commands

```powershell
cd "D:\PLC_effect - Copy"
# High temperature first (fast diffusion)
lmp -in inputs\interface\in.interface_diffusion -var T 900 -log outputs\interface_1k\log_T900_meam.log
# Repeat for 850 K and 700 K
```

To change temperatures, pass `-var T XXX`. Run lengths are controlled by `prod_steps` in the input file.

---

## Post-Processing Workflow

1. **Plot MSD trends**:
   ```powershell
   python scripts\plot_interface_msd.py  # update msd_file path inside as needed
   ```
   Plots saved to `outputs/analysis/msd_trend_interface_TXXX_1k.png`.

2. **Extract diffusivities**:
   ```powershell
   python scripts\analyze_interface_msd.py outputs\interface_1k\msd_interface_T850.dat
   ```
   This reports D and R² for Mg and Al (z-component). Repeat per temperature.

3. **Check MSD quality**:
   ```powershell
   python scripts\check_msd_quality.py --pattern outputs\interface_1k\msd_interface_T*.dat
   ```
   R² values ≥ 0.95 indicate reliable slopes; Mg currently falls short because runs are short.

---

## Limitations and Recommendations

| Issue | Impact | Mitigation |
|-------|--------|------------|
| Short runs (0.4 ns) | Mg MSD plateaus → low R² | Extend to ≥ 0.6 ns or run multiple seeds. |
| Small cross-section (4×4) | High noise; slopes wobble | Generate 6×6 (≈2.3 k atoms) or larger cells. |
| Interface orientation | Our data file uses z as interface normal; ensure analysis scripts use z-component (they do). | N/A |
| MEAM element order | Must specify Al, Mg, Zn in `pair_coeff`; data file only contains types 1–2. | Already handled. |

---

## Future Extensions

- Add automated restart capability for continuing runs to longer times.
- Explore temperature range 650–950 K with identical setups for better Arrhenius coverage.
- Compute RDFs and concentration profiles during the run (or via post-processing) to reproduce Fan et al.’s figures.
- Benchmark against experimental diffusivities by referencing literature values directly in `plot_interface_msd.py`.

---

## Quick Reference

| Task | Command |
|------|---------|
| Create 1 k-atom interface | `python scripts\create_interface_system.py --nx 4 --ny 4 --nz-al 12 --nz-mg 4` |
| MEAM sanity test | `lmp -in inputs\interface\test_meam_minimize.in` |
| Run MD at 850 K | `lmp -in inputs\interface\in.interface_diffusion -var T 850` |
| Analyze MSD | `python scripts\analyze_interface_msd.py outputs\interface_1k\msd_interface_T850.dat` |
| MSD QA summary | `python scripts\check_msd_quality.py --pattern outputs\interface_1k\msd_interface_T*.dat` |

Consult the other READMEs in `docs/` for downstream analyses (Arrhenius, DSA, etc.). For onboarding, have new researchers replicate the 850 K run and confirm their MSD slopes match the current results before moving on.


