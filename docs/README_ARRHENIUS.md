# Arrhenius Fitting and Diffusivity Extrapolation

This guide documents how we convert MD-derived diffusivities into \(D_0\) and \(Q\) parameters, extrapolate to lower temperatures, and track uncertainties.

---

## Goals

1. Fit \( D = D_0 \exp(-Q / (R T)) \) using interface interdiffusion coefficients from the MSD workflow.
2. Provide reproducible scripts for generating plots, parameter tables, and low-temperature extrapolations.
3. Record caveats stemming from limited MD statistics and R² thresholds.

---

## Input Data

- `outputs/analysis/interface_diffusivity_1k.csv`
  - Columns: `T`, `D_Mg`, `R2_Mg`, `D_Al`, `R2_Al`, `D_interdiff`.
  - Currently populated with 700 K, 850 K, 900 K values from the 1 k-atom interface runs (0.1–0.3 ns). Mg R² is < 0.95 at 700/900 K → uncertainties remain high.

---

## Script: `scripts/fit_arrhenius.py`

### Key Features (post-update)

- Accepts any CSV with columns `T` and `D` (or `D_bulk`, `D_interdiff`).
- Performs **log-space linear regression** (ln D vs 1/T), matching manual calculations.
- Optionally filters data based on R² (if provided).
- Outputs:
  - Parameter CSV (`*_params.csv`)
  - Arrhenius plot (`*_species.png`)
  - Extrapolated diffusivities (`*_extrapolated.csv`) for `constants.T_dsa` (300–450 K).

### Default Command

```powershell
python scripts\fit_arrhenius.py ^
    --input outputs/analysis/interface_diffusivity_1k.csv ^
    --species interdiff ^
    --output-prefix outputs/analysis/arrhenius_interface ^
    --extrapolate
```

### Sample Output (current data)

```
D0 = (1.227e-05 +/- 5.425e-05) m^2/s
Q  = (80.54 +/- 29.49) kJ/mol
```

Note: large uncertainties reflect noisy Mg slopes. Extend MD runs to tighten error bars.

---

## Interpreting the Plot

- `*_species.png` includes:
  - Left panel: D vs T (log scale) with fitted curve.
  - Right panel: ln D vs 1/T with regression line.
- Gray markers (if present) indicate data filtered out (e.g., R² below threshold).

---

## Extrapolated Table

`outputs/analysis/arrhenius_interface_interdiff_extrapolated.csv` lists D at 300–450 K (the DSA window). These values feed directly into `analyze_dsa.py`.

| T (K) | D (m²/s) |
|-------|----------|
| 300 | ~6.7×10⁻¹⁵ |
| 350 | ~4.3×10⁻¹⁴ |
| 400 | ~2.2×10⁻¹³ |
| 450 | ~9.4×10⁻¹³ |

(*using current fit; expect increases once MSD quality improves*)

---

## Common Adjustments

| Adjustment | How | Why |
|------------|-----|-----|
| Exclude low-quality data | `--r2-threshold 0.9` (requires columns like `R2_interdiff`) | Remove points dominated by MSD noise. |
| Fit Mg or Al separately | `--species Mg` or `--species Al` | Compare bulk vs interface contributions. |
| No extrapolation | omit `--extrapolate` | Quick parameter-only runs. |
| Alternative input | `--input outputs/analysis/diffusivity_bulk.csv` | Revisit bulk-only analysis. |

---

## Recommended Workflow

1. Run interface MD (700/850/900 K) to completion (≥ 0.6 ns) and update `interface_diffusivity_1k.csv`.
2. Re-run `fit_arrhenius.py` with R² thresholding (e.g., 0.95) once Mg slopes are stable.
3. Store produced plots/CSVs under `outputs/analysis/arrhenius_interface_*`.
4. Feed the extrapolated CSV into `scripts/analyze_dsa.py`.

---

## Troubleshooting

| Symptom | Explanation | Fix |
|---------|-------------|-----|
| `ValueError: Need at least 3 data points` | Input CSV missing/filtered rows | Add more temperatures or lower R² threshold temporarily. |
| Huge errors in D0/Q | Mg R² low (flattened MSD) | Extend runs or enlarge system. |
| Fit values differ from manual log-fit | Ensure script version uses log-space regression (updated). |
| Units confusion | All diffusivities are m²/s; arrhenius outputs Q in kJ/mol and eV/atom for transparency. |

---

## Next Steps

- Add bootstrap resampling to quantify uncertainty from MSD noise.
- Compare interface and bulk Arrhenius fits in a single plot.
- Overlay literature diffusivities for validation, e.g., from Fan et al. or experimental data.

For any updates, modify `scripts/fit_arrhenius.py` and keep this README synchronized with new options or outputs.


