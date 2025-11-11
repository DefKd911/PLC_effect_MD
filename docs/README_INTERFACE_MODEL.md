# Interface Diffusion Model (Al\|Mg Bilayer)

This note explains why we adopted an explicit Al|Mg interface geometry, how it maps to the MEAM potential files, and what assumptions it carries.

---

## Motivation

1. **Reproduce Fan et al. (Physica B 715, 2025)** – their study showed asymmetrical diffusion (Al → Mg > Mg → Al) across a coherent interface. Bulk alloy cells cannot capture this behavior.
2. **Measure interdiffusivity** – interface MSD provides effective Mg-in-Al transport relevant to dislocation atmospheres.
3. **Enable DSA modeling** – interdiffusivity is a key input for capture radius vs waiting distance calculations.

---

## Geometry

| Property | Value | Notes |
|----------|-------|-------|
| Orientation | (100) Al / (100) Mg | Fan et al.’s setup; minimal misfit. |
| Dimensions (default) | 16.2 × 16.2 × 64.8 Å³ | 4×4 FCC cells in x,y; 12 Al + 4 Mg unit cells along z. |
| Atoms | 1 024 (768 Al, 256 Mg) | Configurable via `--nx`, `--ny`, `--nz-al`, `--nz-mg`. |
| Boundaries | Periodic in x,y; fixed boundary layers along z | Top/bottom 5 Å atoms held fixed to prevent drift. |

### Data File Generation

```powershell
python scripts\create_interface_system.py --nx 4 --ny 4 --nz-al 12 --nz-mg 4 ^
    --output inputs\interface\interface_system_small.data
```

To increase statistics, use larger `nx`, `ny` (e.g. 6×6 → 2 304 atoms).

---

## MEAM Potential Mapping

- Files: `potentials/MgAlZn.library.meam`, `potentials/MgAlZn.parameter.meam` (Dickel et al., 2018).
- Three elements declared (Al, Mg, Zn) even if Zn atoms are absent. LAMMPS requires placeholder type 3 with mass assigned in the data file (`interface_system_small.data`).
- Input lines:
  ```lammps
  pair_style meam
  pair_coeff * * potentials/MgAlZn.library.meam Al Mg Zn \
      potentials/MgAlZn.parameter.meam Al Mg Zn
  ```
- Test the potential load via `inputs/interface/test_meam_minimize.in` before production runs.

---

## Why Interface (Not Bulk)

| Aspect | Interface Model | Bulk Random Alloy |
|--------|-----------------|-------------------|
| Asymmetry (Al vs Mg) | Captured via distinct MSD for each species | Averaged out |
| Interdiffusivity | Direct measurement | Requires post-processing of self-diffusion + Darken relation |
| Connection to DSA | Closer to pipe/capture scenario | Only volume diffusion |
| ζ (disorder) | Interface enables concentration/profile analysis | Not applicable |

Given our PLC objective, capturing Al→Mg dominance and interface broadening is essential.

---

## Fixed Layer Justification

The top/bottom 5 Å slabs are immobilized to:
- Prevent bulk translation or rotation.
- Mimic semi-infinite slabs.
- Keep thermostatting restricted to mobile atoms (avoids artifacts).

Drawback: Additional stress near fixed layers. Mitigation: verify temperature/pressure stability (`thermo_style custom step temp pe ...` already in script).

---

## Output Products

| File | Description |
|------|-------------|
| `msd_interface_Txxx.dat` | Columns: step, \( \mathrm{MSD}_{\text{Mg/Al}, x/y/z/total} \). |
| `profile_Mg_Txxx.dat` | Number-density vs z (bin width set by `bin_width`). |
| `traj_interface_Txxx.lammpstrj` | Trajectories for snapshots (e.g., at 0.1, 0.2, 0.4 ns). |
| `log_Txxx_meam.log` | Thermodynamic history (temperature drift, energy, etc.). |

These feed downstream analyses (MSD plots, concentration profiles, eventual RDF calculations).

---

## Known Limitations

1. **Small cross-section** – 4×4 leads to large MSD noise. Use larger cells if resources permit.
2. **Short production** – 0.4 ns insufficient for Mg R² ≥ 0.95 at low T. Plan for 0.6–1.0 ns.
3. **Pipe diffusion not explicit** – currently applied analytically in `analyze_dsa.py`; actual screw/edge dislocations not modeled yet.
4. **No explicit thermally grown disorder** – initial structure is coherent; longer runs or higher T broaden the interface naturally.

---

## Future Enhancements

- Incorporate variable cell sizes (nx, ny) in CI to gauge statistical convergence.
- Automate RDF computation to reproduce Fan et al.’s structural analysis.
- Consider embedding an explicit dislocation line to directly measure pipe diffusion.

See `docs/README_DIFFUSION_MD.md` for run instructions and `docs/README_MSD_QUALITY.md` for QA guidance.


