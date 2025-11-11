"""
Script to analyze MSD data and extract diffusivity.
"""

import numpy as np
import pandas as pd
from scipy import stats
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import (
    T_md,
    msd_r2_threshold,
    timestep_lammps,
    Mg_atomic_percent,
)

def read_msd_file(filename):
    """
    Read MSD data from LAMMPS output file.
    
    Format: TimeStep c_msd_Mg[1-4] c_msd_Al[1-4]
    where [1]=x, [2]=y, [3]=z, [4]=total
    """
    try:
        raw = pd.read_csv(
            filename,
            sep=r'\s+',
            skiprows=3,
            header=None,
            comment='#'
        )

        ncols = raw.shape[1]
        if ncols == 5:
            raw.columns = [
                'step',
                'msd_Mg_x', 'msd_Mg_y', 'msd_Mg_z', 'msd_Mg_total'
            ]
            # Derive Al MSD as NaN to indicate missing data
            for col in ['msd_Al_x', 'msd_Al_y', 'msd_Al_z', 'msd_Al_total']:
                raw[col] = np.nan
        elif ncols >= 9:
            raw = raw.iloc[:, :9]
            raw.columns = [
                'step',
                'msd_Mg_x', 'msd_Mg_y', 'msd_Mg_z', 'msd_Mg_total',
                'msd_Al_x', 'msd_Al_y', 'msd_Al_z', 'msd_Al_total'
            ]
        else:
            raise ValueError(f"Unexpected number of columns ({ncols}) in {filename}")

        return raw
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

def compute_diffusivity(
    msd_data,
    species="Mg",
    timestep=timestep_lammps,
    start_fraction=0.1,
):
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
    time = msd_data["step"].values * timestep  # ps
    
    # Use total MSD (3D)
    column = f"msd_{species}_total"
    if column not in msd_data.columns:
        raise KeyError(f"Column {column} not found in MSD data.")

    msd = msd_data[column].values  # Angstrom²
    if np.all(np.isnan(msd)):
        return None, None, None
    
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
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_s, msd_m2
    )
    
    # Diffusivity = slope / 6
    D = slope / 6.0  # m²/s
    
    r2 = r_value**2
    
    return D, r2, std_err / 6.0

def analyze_all_temperatures(output_dir="outputs/bulk", start_fraction=0.1):
    """
    Analyze MSD data for all temperatures.
    
    Returns:
    --------
    results : DataFrame
        Columns: T, D, D_err, r2, valid
    """
    results = []
    x_Mg = Mg_atomic_percent / 100.0
    x_Al = 1.0 - x_Mg
    
    for T in T_md:
        msd_file = f"{output_dir}/msd_T{T}.dat"
        
        try:
            msd_data = read_msd_file(msd_file)
            if msd_data is None:
                continue

            row = {"T": T}
            for species in ["Mg", "Al"]:
                try:
                    D, r2, D_err = compute_diffusivity(
                        msd_data,
                        species=species,
                        start_fraction=start_fraction,
                    )
                except KeyError as ke:
                    print(f"T = {T} K: Missing data for {species}: {ke}")
                    D = None
                    r2 = None
                    D_err = None
                if D is not None and D <= 0:
                    # Keep track for logging but treat as invalid
                    print(
                        f"T = {T} K ({species}): Non-positive diffusivity ({D:.3e}); marking as invalid."
                    )
                    D = None
                    D_err = None
                    r2 = r2 if r2 is not None else None
                valid = (
                    D is not None
                    and r2 is not None
                    and r2 >= msd_r2_threshold
                )

                row[f"D_{species}"] = D if D is not None else np.nan
                row[f"D_{species}_err"] = (
                    D_err if D_err is not None else np.nan
                )
                row[f"R2_{species}"] = r2 if r2 is not None else np.nan
                row[f"valid_{species}"] = bool(valid)

                if D is not None and r2 is not None:
                    print(
                        f"T = {T} K ({species}): D = {D:.2e} m²/s, R² = {r2:.3f}, Valid = {valid}"
                    )
                else:
                    print(
                        f"T = {T} K ({species}): Insufficient data for diffusivity fit."
                    )

            if row.get("valid_Mg") and row.get("valid_Al"):
                D_inter = x_Mg * row["D_Al"] + x_Al * row["D_Mg"]
                row["D_interdiff"] = D_inter
                row["valid_interdiff"] = True
            else:
                row["D_interdiff"] = np.nan
                row["valid_interdiff"] = False

            results.append(row)

        except Exception as e:
            print(f"Error analyzing T = {T} K: {e}")
            continue
    
    if results:
        df = pd.DataFrame(results)
        ordered_columns = [
            "T",
            "D_Mg",
            "D_Mg_err",
            "R2_Mg",
            "valid_Mg",
            "D_Al",
            "D_Al_err",
            "R2_Al",
            "valid_Al",
            "D_interdiff",
            "valid_interdiff",
        ]
        df = df[ordered_columns]
        return df

    return pd.DataFrame()

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

