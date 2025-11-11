# Dynamic Strain Aging (DSA) and PLC Effect Analysis

This guide explains the theoretical background and the computational steps we use to assess DSA/PLC behavior in Al–5 wt % Mg, including our current prediction and caveats.

---

## Background

- **Dynamic Strain Aging (DSA)** occurs when diffusing solute atoms immobilize dislocations on comparable timescales to dislocation motion.
- **Portevin–Le Châtelier (PLC) effect** manifests as serrated flow in stress–strain curves due to DSA.
- Criterion: compare **diffusion time** \( \tau_{\text{diff}} \) to **waiting time** \( \tau_{\text{wait}} \). Empirical DSA window is \( 0.1 < \tau_{\text{diff}} / \tau_{\text{wait}} < 10 \).

---

## Model Parameters

| Symbol | Meaning | Source |
|--------|---------|--------|
| \(L_c\) | Capture radius (1–5 nm) | `constants.L_capture` |
| \(L_t\) | Travel distance (0.1–10 µm) | `constants.L_travel` |
| \( \rho_m \) | Mobile dislocation density (10¹²–10¹⁴ m⁻²) | `constants.rho_m_values` |
| \( b \) | Burgers vector (2.86×10⁻¹⁰ m) | `constants.b` |
| \( \dot{\varepsilon} \) | Strain rate (10⁻³ s⁻¹) | problem statement |
| \( D_{\text{eff}} \) | Effective diffusivity (includes pipe factor) | Arrhenius extrapolation × (1 + `f_pipe`) |

---

## Workflow

1. **Arrhenius extrapolation**: `scripts/fit_arrhenius.py` → `outputs/analysis/arrhenius_interface_interdiff_extrapolated.csv` at 300–450 K.
2. **DSA analysis**: `scripts/analyze_dsa.py` (updated to accept custom input)
   ```powershell
   python scripts\analyze_dsa.py ^
       --input outputs/analysis/arrhenius_interface_interdiff_extrapolated.csv ^
       --pipe-factor 1.0 ^
       --output outputs/analysis
   ```
3. **Outputs**:
   - `outputs/analysis/dsa_rho...csv`: τ_diff, τ_wait, ratio per temperature and parameter set.
   - `outputs/analysis/tau_comparison.png`: log-log plots comparing τ_diff and τ_wait, and ratio vs T.
   - Console summary highlighting temperature windows satisfying \( 0.1 < \) ratio \( < 10 \).

---

## Current Prediction (v1)

Using current interdiffusivity estimates (log-fit D₀, Q) and **pipe factor = 1.0**:

- For \( \rho_m = 10^{12} \) m⁻², \( L_c = 1 \) nm, \( L_t = 10 \) µm:
  - PLC/DSA likely at **430–450 K**.
- Higher dislocation densities or shorter travel distances shift the window upward (since τ_wait decreases).
- Because Mg R² is < 0.95 at 700/900 K, diffusivities are conservative → DSA range may shift lower after improved simulations.

---

## Equations

\[
\tau_{\text{diff}} = \frac{L_c^2}{D_{\text{eff}}}, \qquad
\tau_{\text{wait}} = \frac{L_t}{\rho_m \, b \, \dot{\varepsilon}}, \qquad
D_{\text{eff}} = D_{\text{bulk}} \times (1 + f_{\text{pipe}})
\]

- \( D_{\text{bulk}} \) is the Arrhenius-extrapolated diffusivity (m² s⁻¹).
- \( f_{\text{pipe}} \) accounts for pipe diffusion (set to 1.0 = doubling D). Adjust via `--pipe-factor`.

---

## Interpreting `tau_comparison.png`

- **Left panel**: log-log curves of τ_diff and τ_wait for representative parameter sets.
- **Right panel**: ratio τ_diff/τ_wait vs T. The shaded region (0.1–10) indicates the PLC-friendly regime.
- Adjusting `--output` in `analyze_dsa.py` allows separate plotting directories per experiment.

---

## Sensitivity Studies

| Parameter | Effect on Ratio | How to Explore |
|-----------|-----------------|----------------|
| \( \rho_m \) ↑ | τ_wait ↓ → easier to meet DSA | Change `rho_m_values` in `constants.py`. |
| \( L_c \) ↑ | τ_diff ↑ → shifts regime to higher T | Update `L_capture` entries. |
| \( L_t \) ↑ | τ_wait ↑ → harder to meet DSA | Adjust `L_travel`. |
| Pipe factor ↑ | τ_diff ↓ (D_eff ↑) | Run `analyze_dsa.py --pipe-factor 2` etc. |
| Diffusivity ↑ (better MSD) | Ratio ↓ | Motivation for improved MD runs. |

---

## PLC Prediction Summary (to date)

- **Temperature window** (nominal parameters): 430–450 K indicates the PLC effect is likely in mid-range service temperatures.
- **Uncertainty**: Dominated by diffusivity errors and the choice of length scales. Document each assumption when reporting results.
- **Next steps**:
  1. Improve Mg R² via longer simulations → recalc Arrhenius → rerun DSA.
  2. Compare with experimental PLC maps (literature) to validate the predicted window.
  3. Integrate creep/slip models if we want stress–strain serration predictions.

---

## References and Further Reading

- Fan et al., *Physica B* **715**, 417620 (2025).
- Dickel et al., *Modelling Simul. Mater. Sci. Eng.* **26**, 045010 (2018).
- Classical DSA theory: e.g., Kubin & Estrin, *Acta Metall.* 38 (1990).

---

Use this README in tandem with `docs/README_ARRHENIUS.md` (data source) and `docs/README_DIFFUSION_MD.md` (simulation details). Update the conclusions whenever diffusivity inputs or material parameters change.


