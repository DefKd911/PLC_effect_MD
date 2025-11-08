# How to Stop a Running LAMMPS Simulation

## If Simulation is Running in Terminal

### Windows PowerShell:
Press `Ctrl + C` to stop the simulation

### What Happens:
- The simulation will stop at the current step
- Partial output files will be saved
- You can analyze the data that was collected so far

## Current Simulation Status

Your simulation is currently running with:
- **Equilibration:** 50,000 steps (50 ps) - Currently in this phase
- **Production:** 10,000,000 steps (10 ns) - Will take hours/days!

## Options

### Option 1: Stop Current Run and Use Quick Test Version

1. **Stop the simulation:** Press `Ctrl + C` in the terminal
2. **Run quick test version:**
   ```bash
   lmp -in inputs/bulk/in.bulk_diffusion.quick -log outputs/bulk/log_T800_quick.log
   ```
   This will run:
   - 10 ps equilibration (instead of 50 ps)
   - 0.1 ns production (instead of 10 ns)
   - Total time: ~5-10 minutes instead of hours

### Option 2: Let Current Run Continue

If you want to let it run:
- It will take several hours to complete
- You'll get better quality data
- For a full production run, this is appropriate

### Option 3: Modify Current Input File

Edit `inputs/bulk/in.bulk_diffusion`:
- Change `run 10000000` to `run 100000` (0.1 ns instead of 10 ns)
- Change `run 50000` to `run 10000` (10 ps instead of 50 ps)

## Recommended for Testing

**Use the quick version first:**
```bash
# Stop current run (Ctrl+C)
# Then run:
lmp -in inputs/bulk/in.bulk_diffusion.quick -log outputs/bulk/log_T800_quick.log
```

This will:
- ✅ Complete in 5-10 minutes
- ✅ Generate MSD data you can analyze
- ✅ Verify everything works
- ✅ Then you can run full 10 ns simulations later

## For Production Runs

Once you've verified everything works:
- Use the original `in.bulk_diffusion` file
- Run overnight or on a cluster
- 10 ns is appropriate for accurate diffusivity measurements


