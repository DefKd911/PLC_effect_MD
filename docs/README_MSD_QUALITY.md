# MSD Quality Assurance and Diagnostics

Mean-squared displacement (MSD) quality directly controls the reliability of our diffusivity estimates. This README outlines how we evaluate MSD data, interpret warnings, and plan reruns.

---

## Tools

| Script | Purpose |
|--------|---------|
| `scripts/analyze_interface_msd.py` | Computes D and R² for Mg/Al (z-component). |
| `scripts/check_msd_quality.py` | Summarizes time span, MSD range, and linear fit quality. |
| `scripts/plot_interface_msd.py` | Visualizes MSD vs time with best-fit lines. |

---

## Quality Criteria

1. **R² threshold**: `constants.msd_r2_threshold = 0.95`. Values below indicate noisy or insufficiently long runs.
2. **Positive slope**: Diffusivity must be > 0; negative slopes typically mean the MSD is still oscillating around a plateau.
3. **Time window**: Aim for ≥ 0.4 ns of production data (0.6 ns preferred at 700 K) to capture steady-state diffusion.
4. **Directional consistency**: Use the interface-normal component (z) for interdiffusion analysis.

---

## Workflow Checklist

1. **Run analyzer per temperature**:
   ```powershell
   python scripts\analyze_interface_msd.py outputs\interface_1k\msd_interface_T850.dat
   ```
   Record D, R², and number of points.

2. **Batch QA**:
   ```powershell
   python scripts\check_msd_quality.py --pattern outputs\interface_1k\msd_interface_T*.dat
   ```
   Output includes time range, MSD amplitude, and rough diffusivity estimates.

3. **Inspect plots**:
   - `outputs/analysis/msd_trend_interface_T850_1k.png`, etc.
   - Confirm linear growth after discarding the first 20 % of data (the script automatically skips the transient).

---

## Interpreting Warnings

| Warning | Meaning | Action |
|---------|---------|--------|
| `R^2 < 0.8` | MSD essentially flat or noisy | Extend run, increase cell size, or average multiple seeds. |
| Negative slope in plot | Simulation too short; minimal diffusion events | Continue run until MSD shows net growth. |
| MSD change < 1 Å² after 0.1 ns | Diffusion extremely slow at this temperature | Increase temperature for validation first, then revisit low T. |

---

## Mitigation Strategies

1. **Longer production**: Increase `prod_steps` in `in.interface_diffusion` (e.g., 600 000–1 000 000).
2. **Larger cross-section**: Use `--nx 6 --ny 6` when building the data file to reduce statistical noise.
3. **Multiple seeds**: Run independent simulations with different velocity seeds and average MSDs (script support pending).
4. **Post-fit filtering**: When fitting Arrhenius, use `--r2-threshold` to exclude noisy points and document the exclusion.

---

## Tracking Improvements

- Maintain a table (e.g., in `outputs/analysis/interface_diffusivity_history.csv`) with date, temperature, run length, R², and notes.
- Commit MSD plots for each iteration so trends are visually traceable.
- Update this README if new QA metrics or automated checks are introduced.

---

## Future Enhancements

- Automate R² gating in `analyze_interface_msd.py` (currently manual).
- Compute MSD confidence intervals (bootstrap or block averaging) for error bars on D.
- Integrate QA into CI pipelines (e.g., fail if R² < threshold).

For new contributors, the recommended first task is to re-run `check_msd_quality.py` after any MD simulation and verify that Mg R² meets the target before proceeding to Arrhenius fitting.


