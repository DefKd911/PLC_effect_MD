# Updated Workflow Per Professor Feedback

## Key Changes

### ✅ Approved Approach
1. **3 temperatures only** (not 5-6) - sufficient for Arrhenius fit
2. **Temperature range: 500, 600, 700 K** (below Al melting ~933 K)
3. **No dislocation MD simulations** - use analytical pipe diffusion factor
4. **Two separate L values**:
   - **L_c**: Capture radius (nm scale, ~1-5 nm) for τ_diff
   - **L_t**: Travel distance (µm scale, ~0.1-10 µm) for τ_wait
5. **Shorter simulations**: 0.1 ns equilibration, 5 ns production

### ❌ Removed/Simplified
- Dislocation core diffusion MD simulations
- Binding energy calculations (can use literature values for L_c)
- Multiple temperature points (reduced to 3)

## Updated Workflow

### Step 1: Bulk Diffusion MD (3 temperatures)

**Temperatures:** 500 K, 600 K, 700 K

**Simulation parameters:**
- Equilibration: 0.1 ns (100,000 steps)
- Production: 5 ns (5,000,000 steps)
- Total per temperature: ~5-8 hours

**Output:** D(T) at 3 temperatures

### Step 2: Arrhenius Fit

Fit: D = D₀ × exp(-Q/(R×T))

**Output:** D₀ and Q (activation energy)

### Step 3: Analytical Pipe Diffusion Correction

D_eff = D_bulk × (1 + f_pipe)

Where f_pipe = 0.1-10 (default 1.0 for pure bulk)

### Step 4: DSA Analysis with Two L Values

**τ_diff = L_c² / D_eff**
- L_c: Capture radius (1-5 nm)
- D_eff: Effective diffusivity

**τ_wait = L_t / (ρ_m × b × ε̇)**
- L_t: Travel distance (0.1-10 µm)
- ρ_m: Mobile dislocation density (10¹²-10¹⁴ m⁻²)
- b: Burgers vector (2.86×10⁻¹⁰ m)
- ε̇: Strain rate (10⁻³ s⁻¹)

**DSA occurs when:** τ_diff ≈ τ_wait

### Step 5: Report

- Arrhenius plot (ln D vs 1/T)
- Fitted D₀ and Q
- τ_diff vs τ_wait comparison
- DSA temperature window identification

## Computational Plan

| Stage | Task | # Runs | Duration | Purpose |
|-------|------|--------|----------|---------|
| 1 | Bulk diffusion at 500 K | 1 | ~5-8 hrs | D₁ |
| 2 | Bulk diffusion at 600 K | 1 | ~5-8 hrs | D₂ |
| 3 | Bulk diffusion at 700 K | 1 | ~5-8 hrs | D₃ |
| — | Fit Arrhenius | — | Post-processing | D₀, Q |
| — | DSA analysis | — | Python script | No MD |

**Total:** ~15-24 hours of MD simulation time

## Next Immediate Steps

1. ✅ Update constants.py (DONE)
2. ✅ Update LAMMPS input files (DONE)
3. ✅ Update DSA analysis script (DONE)
4. ⏳ Run test at 500 K (0.1 ns test)
5. ⏳ Run full 5 ns simulations at 500, 600, 700 K
6. ⏳ Analyze MSD → D(T)
7. ⏳ Fit Arrhenius
8. ⏳ Run DSA analysis with two L values
9. ⏳ Generate final report

## Files Updated

- `constants.py` - New temperature range, simulation times, L values
- `inputs/bulk/in.bulk_diffusion` - Shorter equilibration/production
- `scripts/analyze_dsa.py` - Two L values, analytical pipe diffusion

## Notes

- No need to run dislocation simulations
- Can use literature values for L_c (capture radius) if needed
- Pipe diffusion factor f_pipe can be varied for sensitivity analysis
- Focus is on accurate bulk D(T) from MD, then analytical DSA model

