# How to Run Simulations - Detailed Instructions

## Method 1: Using Variable (Recommended)

The input file uses LAMMPS variables. You can set temperature via command line:

```bash
# Temperature 500 K
lmp -in inputs/bulk/in.bulk_diffusion -var T 500 -log outputs/bulk/log_T500.log

# Temperature 600 K
lmp -in inputs/bulk/in.bulk_diffusion -var T 600 -log outputs/bulk/log_T600.log

# Temperature 700 K
lmp -in inputs/bulk/in.bulk_diffusion -var T 700 -log outputs/bulk/log_T700.log
```

## Method 2: Edit Input File Directly

Alternatively, edit the input file before each run:

1. Open `inputs/bulk/in.bulk_diffusion`
2. Change line 7: `variable T equal 500` (or 600, or 700)
3. Save file
4. Run: `lmp -in inputs/bulk/in.bulk_diffusion -log outputs/bulk/log_T500.log`

## What Happens During Simulation

### Phase 1: Equilibration (0.1 ns = 100,000 steps)
- System heated to target temperature
- Pressure and volume equilibrate
- Takes ~10-20 minutes

### Phase 2: Production (1 ns = 100,000 steps)
- System runs at constant temperature
- MSD data collected every 1000 steps
- Takes ~1-2 hours total

### Output Files Created

For each temperature T:
- `outputs/bulk/msd_T{T}.dat` - MSD data (needed for analysis)
- `outputs/bulk/traj_T{T}.lammpstrj` - Trajectory (optional, large file)
- `outputs/bulk/log_T{T}.log` - Complete log file

## Monitoring Progress

While simulation runs, you can check progress:

```bash
# Check log file (last few lines)
tail -20 outputs/bulk/log_T500.log

# Check if MSD file is being written
ls -lh outputs/bulk/msd_T500.dat
```

## When Simulation is Done

You'll see in the log:
```
Simulation completed at T = 500 K
MSD data written to: outputs/bulk/msd_T500.dat
```

Then proceed to analysis!

