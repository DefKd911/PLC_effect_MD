"""
Quick script to check MSD data quality.
"""

import pandas as pd
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_msd_file(filename):
    """Check MSD file quality."""
    try:
        df = pd.read_csv(filename, sep=r'\s+', skiprows=2, 
                        names=['step', 'msd_x', 'msd_y', 'msd_z', 'msd_total'],
                        comment='#')
        
        # Convert step to time (ps)
        time = df['step'].values * 0.001  # ps
        msd = df['msd_total'].values  # Angstrom^2
        
        # Check basic statistics
        print(f"\nFile: {filename}")
        print("=" * 60)
        print(f"Data points: {len(df)}")
        print(f"Time range: {time[0]:.1f} to {time[-1]:.1f} ps ({time[-1]/1000:.3f} ns)")
        print(f"MSD range: {msd.min():.3f} to {msd.max():.3f} Angstrom^2")
        print(f"MSD change: {msd[-1] - msd[0]:.3f} Angstrom^2")
        
        # Check if MSD is increasing
        if msd[-1] > msd[0]:
            print(f"[OK] MSD is increasing (good sign)")
        else:
            print(f"[WARNING] MSD is not increasing - may indicate no diffusion")
        
        # Check linearity (simple check)
        from scipy import stats
        slope, intercept, r_value, p_value, std_err = stats.linregress(time, msd)
        r2 = r_value ** 2
        
        print(f"Linear fit R^2: {r2:.4f}")
        if r2 > 0.95:
            print(f"[OK] Good linearity (R^2 > 0.95)")
        elif r2 > 0.8:
            print(f"[WARNING] Moderate linearity (R^2 = {r2:.3f})")
        else:
            print(f"[WARNING] Poor linearity (R^2 = {r2:.3f}) - may need longer simulation")
        
        # Check if values are reasonable
        # At 800 K, MSD after 0.06 ns should be growing
        if msd[-1] < 1.0:
            print(f"[WARNING] MSD values are very small (< 1 Angstrom^2)")
            print(f"  This might indicate:")
            print(f"  - Simulation too short")
            print(f"  - Temperature too low for measurable diffusion")
            print(f"  - System not properly equilibrated")
        
        # Estimate diffusivity (rough)
        if r2 > 0.5 and msd[-1] > msd[0]:
            # D = slope / 6 (convert Angstrom^2/ps to m^2/s)
            D_rough = (slope / 6.0) * 1e-20  # Angstrom^2/ps to m^2/s
            print(f"Rough diffusivity estimate: {D_rough:.2e} m^2/s")
        
        return df, r2
        
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None, None

if __name__ == "__main__":
    import glob
    
    print("Checking MSD Data Quality")
    print("=" * 60)
    
    # Check all MSD files
    msd_files = glob.glob("outputs/bulk/msd_T*.dat")
    
    if len(msd_files) == 0:
        print("No MSD files found in outputs/bulk/")
    else:
        for f in sorted(msd_files):
            check_msd_file(f)
    
    print("\n" + "=" * 60)
    print("Summary:")
    print("Good MSD data should:")
    print("  1. Increase linearly with time")
    print("  2. Have R^2 > 0.95 for linear fit")
    print("  3. Show clear growth over simulation time")
    print("  4. Values should be reasonable for temperature")

