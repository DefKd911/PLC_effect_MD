# MEAM Potential Usage Guide

This README captures the provenance and correct usage of the Mg–Al–Zn MEAM potential employed throughout the project.

---

## Source

- **Reference**: Dickel et al., *Modeling and Simulation in Materials Science and Engineering* **26**, 045010 (2018).
- **Files**: Provided with the supplementary material of the publication; stored in `potentials/` as:
  - `MgAlZn.library.meam`
  - `MgAlZn.parameter.meam`

---

## Why MEAM?

1. Supports angular forces necessary to capture interfacial energetics between Al and Mg.
2. Reproduces melting points near experimental values (Al ≈ 933 K, Mg ≈ 925 K), as confirmed by quick heating tests.
3. Consistent with Fan et al. (2025), enabling qualitative comparisons.

---

## Integration in LAMMPS

```lammps
pair_style meam
pair_coeff * * potentials/MgAlZn.library.meam Al Mg Zn \
    potentials/MgAlZn.parameter.meam Al Mg Zn
```

### Important Notes

- LAMMPS requires a placeholder element (Zn) even if the system contains only Al and Mg. The data file should declare three atom types with masses:
  ```
  1 26.98  # Al
  2 24.31  # Mg
  3 65.38  # Zn (unused placeholder)
  ```
- The order of element names after `pair_coeff * *` **must** match the atom types in the data file.
- If `pair_coeff` throws “Cmax out of range” errors, double-check that the third element (Zn) is included.

---

## Sanity Checks

1. Run `inputs/interface/test_meam_minimize.in` to verify the potential loads and a mixed Al/Mg box minimizes without errors.
2. Optionally reproduce melting curves by gradually heating pure Al/Mg cells (per Fan et al.’s validation).

---

## Common Pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Error in MEAM parameter file` | Missing Zn placeholder or wrong order | Ensure `pair_coeff * * ... Al Mg Zn` and data file has 3 types. |
| Unexpected forces on fixed layers | Forgetting to exclude fixed atoms from thermostat | Use groups as in `in.interface_diffusion`. |
| Different total energy than reference | LAMMPS version differences | Confirm you’re on 22 Jul 2025 build (same as current logs). |

---

## Potential Alternatives

- **EAM/FS**: easier to load but lacks angular dependence; prior tests showed underestimation of vacancy energetics and incorrect interface behavior.
- **MEAM from other authors**: possible, but we prioritized matching the 2018 potential to align with literature benchmarks.

---

## Best Practices

1. Keep the `potentials/` directory under version control; document any modifications.
2. Store download or conversion scripts (if any) alongside this README.
3. Reference this document from other READMEs to avoid repeating setup details.

If new potentials are introduced, append sections describing their validation steps and compatibility with existing data. Update the interface README to reflect any changes in element ordering or masses.


