"""
Script to analyze MSD data and extract diffusivity.
"""

import numpy as np
import pandas as pd
from scipy import stats
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import T_md, msd_r2_threshold

def read_msd_file(filename):
    """
    Read MSD data from LAMMPS output file.
    
    Format: TimeStep c_msd_Mg[1] c_msd_Mg[2] c_msd_Mg[3] c_msd_Mg[4]
    where [1]=x, [2]=y, [3]=z, [4]=total
    """
    try:
        data = pd.read_csv(filename, sep=r'\s+', skiprows=3, 
                          names=['step', 'msd_x', 'msd_y', 'msd_z', 'msd_total'],
                          comment='#')
        return data
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def compute_diffusivity(msd_data, timestep=0.001, start_fraction=0.1):
    """
    Compute diffusivity from MSD data using Einstein relation.
    
    D = (1/6) * d(MSD)/dt
    
    Parameters:
    -----------
    msd_data : DataFrame
        MSD data with columns: step, msd_x, msd_y, msd_z, msd_total
    timestep : float
        Time step in ps
    start_fraction : float
        Fraction of data to skip at start (to avoid equilibration effects)
    
    Returns:
    --------
    D : float
        Diffusivity in m²/s
    r2 : float
        R² value of linear fit
    std_err : float
        Standard error of fit
    """
    # Convert step to time (ps)
    time = msd_data['step'].values * timestep  # ps
    
    # Use total MSD (3D)
    msd = msd_data['msd_total'].values  # Angstrom²
    
    # Skip initial portion
    start_idx = int(len(time) * start_fraction)
    time = time[start_idx:]
    msd = msd[start_idx:]
    
    if len(time) < 10:
        return None, None, None
    
    # Convert MSD from Angstrom² to m²
    msd_m2 = msd * 1e-20  # Angstrom² to m²
    
    # Convert time from ps to s
    time_s = time * 1e-12  # ps to s
    
    # Linear fit: MSD = 6*D*t
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_s, msd_m2)
    
    # Diffusivity = slope / 6
    D = slope / 6.0  # m²/s
    
    r2 = r_value ** 2
    
    return D, r2, std_err / 6.0

def analyze_all_temperatures(output_dir="outputs/bulk"):
    """
    Analyze MSD data for all temperatures.
    
    Returns:
    --------
    results : DataFrame
        Columns: T, D, D_err, r2, valid
    """
    results = []
    
    for T in T_md:
        msd_file = f"{output_dir}/msd_T{T}.dat"
        
        try:
            msd_data = read_msd_file(msd_file)
            if msd_data is None:
                continue
            
            D, r2, D_err = compute_diffusivity(msd_data)
            
            if D is None:
                continue
            
            # Check if fit is valid
            valid = r2 >= msd_r2_threshold
            
            results.append({
                'T': T,
                'D': D,
                'D_err': D_err if D_err else 0.0,
                'r2': r2,
                'valid': valid
            })
            
            print(f"T = {T} K: D = {D:.2e} m²/s, R² = {r2:.3f}, Valid = {valid}")
            
        except Exception as e:
            print(f"Error analyzing T = {T} K: {e}")
            continue
    
    df = pd.DataFrame(results)
    return df

def save_results(df, filename="outputs/analysis/diffusivity_bulk.csv"):
    """Save diffusivity results to CSV."""
    import os
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    df.to_csv(filename, index=False)
    print(f"\nResults saved to {filename}")

if __name__ == "__main__":
    print("Analyzing MSD data for bulk diffusion...")
    print("=" * 60)
    
    df = analyze_all_temperatures()
    
    if len(df) > 0:
        print(f"\nAnalyzed {len(df)} temperatures")
        print("\nResults:")
        print(df.to_string(index=False))
        
        save_results(df)
    else:
        print("No valid data found. Please run simulations first.")

