# MSD Data Quality Issues - Analysis

## Current MSD Data Problems

### T800 Data (from old simulation):
- **Time range:** Only 0.06 ns (should be 1 ns)
- **MSD trend:** NOT increasing (actually decreasing slightly)
- **R²:** 0.006 (very poor - should be > 0.95)
- **MSD values:** 0.92-0.96 Angstrom² (oscillating, not growing)

### T500 Data (new simulation):
- **Time range:** Only 0.113 ns (should be 1 ns)
- **MSD trend:** NOT increasing
- **R²:** 0.058 (very poor)
- **MSD values:** 0.079-0.096 Angstrom² (very small, oscillating)

## What's Wrong?

### 1. Simulations Too Short
- **Expected:** 1 ns production (100,000 steps)
- **Actual:** Only 0.06-0.113 ns
- **Problem:** Simulation stopped early or didn't complete

### 2. MSD Not Growing
- **Expected:** MSD should increase linearly with time
- **Actual:** MSD is oscillating around a constant value
- **Problem:** This looks like thermal fluctuations, not diffusion

### 3. Poor Linearity
- **Expected:** R² > 0.95 for good diffusion data
- **Actual:** R² = 0.006-0.058
- **Problem:** No clear diffusion behavior

## Why This Happens

1. **Simulation too short:** Need full 1 ns to see diffusion
2. **Temperature might be too low:** At 500 K, diffusion is slow
3. **System might not be equilibrated:** MSD starts from non-zero (should start near 0)
4. **MSD calculation issue:** May be computing from wrong reference

## What Good MSD Data Should Look Like

### Good Example:
```
Time (ps)    MSD (Angstrom²)
0            0.0
10           0.5
20           1.0
30           1.5
40           2.0
...
100          5.0
```

**Characteristics:**
- Starts near 0
- Increases linearly
- R² > 0.95
- Clear upward trend

### Your Current Data:
```
Time (ps)    MSD (Angstrom²)
10           0.95
20           0.94
30           0.95
...
60           0.93
```

**Problems:**
- Starts at ~0.95 (not 0)
- No clear growth
- Oscillating around constant value

## Solutions

### 1. Check Why Simulation Stopped Early

```bash
# Check log file for errors
tail -50 outputs/bulk/log_T500.log

# Check if simulation completed
grep "Simulation completed" outputs/bulk/log_T500.log
```

### 2. Ensure Full 1 ns Production Run

The input file should have:
```
run 100000  # 1 ns production (100,000 steps)
```

### 3. Check MSD Calculation

The MSD should be computed from initial positions. Check:
- MSD should start near 0 (after equilibration)
- Should grow linearly during production

### 4. For Higher Temperatures

At 500 K, diffusion is slow. Consider:
- Running longer (2-3 ns instead of 1 ns)
- Or focus on 600-700 K where diffusion is faster

## Next Steps

1. **Check current T500 simulation:**
   ```bash
   tail -20 outputs/bulk/log_T500.log
   ```
   See if it's still running or stopped

2. **If stopped early:** Restart with full 1 ns

3. **For new simulations:** Make sure they run full 100,000 steps

4. **Expected MSD at 700 K:** Should show clearer growth than 500 K

## Expected MSD Values

At higher temperatures, MSD should be:
- **700 K:** MSD ~ 5-20 Angstrom² after 1 ns
- **600 K:** MSD ~ 2-10 Angstrom² after 1 ns  
- **500 K:** MSD ~ 1-5 Angstrom² after 1 ns (slower)

Your current values (0.1-1 Angstrom²) suggest:
- Simulation too short, OR
- Temperature too low, OR
- MSD calculation issue

