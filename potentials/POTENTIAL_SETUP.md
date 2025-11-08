# Potential File Setup - COMPLETED ✓

## Your Potential File

**File:** `potentials/Al-Mg.eam.fs`

**Source:** Mendelev et al. (2009) from NIST repository
- **Reference:** M.I. Mendelev, M. Asta, M.J. Rahman and J.J. Hoyt, Phil. Mag. 89, 3269-3285 (2009)
- **Downloaded from:** https://www.ctcms.nist.gov/potentials/Download/2009--Mendelev-M-I-Asta-M-Rahman-M-J-Hoyt-J-J--Al-Mg/1/Al-Mg.eam.fs

## Status: ✓ READY TO USE

The potential file has been verified and all scripts have been updated to use it correctly.

### Changes Made

1. ✅ Updated all LAMMPS input files to use `pair_style eam/fs` (instead of `eam/alloy`)
2. ✅ Updated potential file path to `potentials/Al-Mg.eam.fs` in all scripts
3. ✅ Verified file format is correct (Finnis-Sinclair EAM format)

### File Format

- **Format:** `.eam.fs` (Finnis-Sinclair EAM)
- **Pair Style:** `eam/fs` (in LAMMPS)
- **Elements:** Al and Mg
- **Compatible:** Yes, with all simulation scripts

## Next Steps

You can now run simulations:

```bash
# Create systems
python scripts/create_bulk_system.py

# Run simulations (if LAMMPS is installed)
python scripts/run_bulk_diffusion.py

# Or run manually:
lmp -in inputs/bulk/in.bulk_diffusion -log outputs/bulk/log_T800.log
```

## Verification

The potential file is:
- ✅ Correct format (Finnis-Sinclair EAM)
- ✅ From reputable source (Mendelev et al. 2009)
- ✅ Appropriate for Al-Mg diffusion studies
- ✅ Compatible with all project scripts

No further action needed - you're ready to run simulations!


