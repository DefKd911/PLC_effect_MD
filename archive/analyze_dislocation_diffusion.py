"""
Script to analyze MSD data for Mg atoms in radial bins around dislocation.
"""

import numpy as np
import pandas as pd
from scipy import stats
from constants import T_md, msd_r2_threshold, radial_bins
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_msd import compute_diffusivity

def read_radial_msd_file(filename):
    """
    Read radial MSD data from LAMMPS output.
    
    Format: TimeStep msd_core msd_near msd_far msd_bulk
    """
    try:
        data = pd.read_csv(filename, sep=r'\s+', skiprows=3,
                          names=['step', 'msd_core', 'msd_near', 'msd_far', 'msd_bulk'],
                          comment='#')
        return data
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def analyze_radial_diffusion(output_dir="outputs/dislocation"):
    """
    Analyze MSD data for different radial bins.
    
    Returns:
    --------
    results : dict
        Dictionary with temperature as key, each containing:
        {'r_bin': [r values], 'D': [D values], 'r2': [r2 values]}
    """
    results = {}
    
    for T in T_md:
        msd_file = f"{output_dir}/msd_radial_T{T}.dat"
        
        try:
            msd_data = read_radial_msd_file(msd_file)
            if msd_data is None:
                continue
            
            # Analyze each radial bin
            bin_names = ['core', 'near', 'far', 'bulk']
            r_centers = [0.25, 0.75, 1.5, 3.0]  # nm (center of each bin)
            
            D_values = []
            r2_values = []
            r_vals = []
            
            for bin_name, r_center in zip(bin_names, r_centers):
                msd_col = f'msd_{bin_name}'
                if msd_col not in msd_data.columns:
                    continue
                
                # Create temporary DataFrame for this bin
                bin_data = pd.DataFrame({
                    'step': msd_data['step'],
                    'msd_total': msd_data[msd_col]
                })
                
                D, r2, _ = compute_diffusivity(bin_data)
                
                if D is not None and r2 >= msd_r2_threshold:
                    D_values.append(D)
                    r2_values.append(r2)
                    r_vals.append(r_center)
            
            if len(D_values) > 0:
                results[T] = {
                    'r': np.array(r_vals),
                    'D': np.array(D_values),
                    'r2': np.array(r2_values)
                }
                print(f"T = {T} K: Analyzed {len(D_values)} radial bins")
        
        except Exception as e:
            print(f"Error analyzing T = {T} K: {e}")
            continue
    
    return results

def extract_core_diffusivity(results):
    """
    Extract diffusivity at dislocation core (innermost bin) for each temperature.
    
    Returns:
    --------
    df : DataFrame
        Columns: T, D_core, D_core_err, r2
    """
    data = []
    
    for T, res in results.items():
        if len(res['r']) > 0:
            # Core is the innermost bin (smallest r)
            idx = np.argmin(res['r'])
            data.append({
                'T': T,
                'D_core': res['D'][idx],
                'r2': res['r2'][idx],
                'r_bin': res['r'][idx]
            })
    
    return pd.DataFrame(data)

def compute_enhancement_factor(D_core_df, D_bulk_df):
    """
    Compute pipe diffusion enhancement factor f = D_core / D_bulk.
    
    Parameters:
    -----------
    D_core_df : DataFrame
        Core diffusivity data (columns: T, D_core)
    D_bulk_df : DataFrame
        Bulk diffusivity data (columns: T, D)
    
    Returns:
    --------
    df : DataFrame
        Enhancement factor data
    """
    # Merge on temperature
    merged = pd.merge(D_core_df, D_bulk_df, on='T', how='inner')
    merged['f'] = merged['D_core'] / merged['D']
    
    return merged[['T', 'D_core', 'D', 'f']]

def save_results(results, core_df, enhancement_df, output_dir="outputs/analysis"):
    """Save all dislocation diffusion results."""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Save radial profiles
    all_radial_data = []
    for T, res in results.items():
        for r, D, r2 in zip(res['r'], res['D'], res['r2']):
            all_radial_data.append({'T': T, 'r': r, 'D': D, 'r2': r2})
    
    if all_radial_data:
        pd.DataFrame(all_radial_data).to_csv(
            f"{output_dir}/diffusivity_radial.csv", index=False)
    
    # Save core diffusivity
    core_df.to_csv(f"{output_dir}/diffusivity_core.csv", index=False)
    
    # Save enhancement factor
    enhancement_df.to_csv(f"{output_dir}/enhancement_factor.csv", index=False)

def main():
    """Main function."""
    print("Analyzing dislocation core diffusion...")
    print("=" * 60)
    
    # Analyze radial MSD data
    results = analyze_radial_diffusion()
    
    if len(results) == 0:
        print("No valid data found. Please run dislocation simulations first.")
        return
    
    # Extract core diffusivity
    core_df = extract_core_diffusivity(results)
    print(f"\nCore diffusivity extracted for {len(core_df)} temperatures")
    
    # Load bulk diffusivity for comparison
    try:
        bulk_df = pd.read_csv("outputs/analysis/diffusivity_bulk.csv")
        bulk_df = bulk_df[bulk_df['valid'] == True][['T', 'D']]
        
        # Compute enhancement factor
        enhancement_df = compute_enhancement_factor(core_df, bulk_df)
        print(f"\nEnhancement factor computed:")
        print(enhancement_df.to_string(index=False))
        
    except FileNotFoundError:
        print("Warning: bulk diffusivity data not found. Skipping enhancement factor.")
        enhancement_df = pd.DataFrame()
    
    # Save results
    save_results(results, core_df, enhancement_df)
    print("\nResults saved to outputs/analysis/")

if __name__ == "__main__":
    main()

