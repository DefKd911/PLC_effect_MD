"""
Script to compute/validate L_c (capture radius) and L_t (travel distance) values.
These are two DIFFERENT length scales with different physical meanings.
"""

import numpy as np
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import k_B, L_capture, L_travel

def compute_L_c_from_binding_energy(E_b, T):
    """
    Compute capture radius L_c from binding energy.
    
    L_c is the distance where binding energy E_b ≈ k_B*T.
    This represents the effective capture distance for solutes.
    
    Parameters:
    -----------
    E_b : float or array
        Binding energy (eV)
    T : float or array
        Temperature (K)
    
    Returns:
    --------
    L_c : float or array
        Capture radius (m)
    """
    # Simple model: L_c ≈ r where E_b(r) = k_B*T
    # For a more detailed model, would need E_b(r) curve
    # For now, use literature values or simple estimate
    
    # Typical values from literature for Al-Mg:
    # L_c ≈ 1-5 nm at room temperature
    # Scales roughly as: L_c(T) ≈ L_c(300K) * sqrt(300/T)
    
    L_c_300K = 2.0e-9  # 2 nm at 300 K (typical value)
    L_c = L_c_300K * np.sqrt(300.0 / T)
    
    return L_c

def compute_L_t_from_microstructure(rho_m, b, epsilon_dot, T):
    """
    Compute travel distance L_t from microstructure parameters.
    
    L_t is the average distance a dislocation travels before being pinned.
    This depends on dislocation density, strain rate, and temperature.
    
    Parameters:
    -----------
    rho_m : float or array
        Mobile dislocation density (m⁻²)
    b : float
        Burgers vector (m)
    epsilon_dot : float
        Strain rate (s⁻¹)
    T : float or array
        Temperature (K)
    
    Returns:
    --------
    L_t : float or array
        Travel distance (m)
    """
    # Simple model: L_t ≈ v * τ_wait
    # Where v = dislocation velocity
    # For a more detailed model, would need dislocation dynamics
    
    # Typical values from literature:
    # L_t ≈ 0.1-10 µm depending on conditions
    
    # Simple estimate based on strain rate:
    # L_t ≈ (strain rate) / (rho_m * b) * (some time scale)
    # Or use empirical relation from literature
    
    # For Al-Mg at ε̇ = 10⁻³ s⁻¹:
    # Typical L_t ≈ 1-10 µm
    
    # Use middle value as default, can be varied
    L_t = 1.0e-6  # 1 µm (typical value)
    
    return L_t

def get_literature_values():
    """
    Get typical L_c and L_t values from literature for Al-Mg system.
    
    Returns:
    --------
    L_c_range : tuple
        (L_c_min, L_c_max) in meters
    L_t_range : tuple
        (L_t_min, L_t_max) in meters
    """
    # Literature values for Al-Mg:
    # L_c (capture radius): 1-5 nm typically
    # L_t (travel distance): 0.1-10 µm typically
    
    L_c_min = 1.0e-9  # 1 nm
    L_c_max = 5.0e-9  # 5 nm
    
    L_t_min = 0.1e-6  # 0.1 µm
    L_t_max = 10.0e-6  # 10 µm
    
    return (L_c_min, L_c_max), (L_t_min, L_t_max)

def validate_length_scales():
    """
    Validate that L_c and L_t are properly differentiated.
    """
    print("=" * 60)
    print("Length Scale Validation")
    print("=" * 60)
    
    print("\nL_c (Capture Radius) - for tau_diff:")
    print(f"  Values: {L_capture * 1e9} nm")
    print(f"  Physical meaning: Distance for solute capture by dislocation")
    print(f"  Used in: tau_diff = L_c^2 / D_eff")
    print(f"  Scale: nanometers (nm)")
    
    print("\nL_t (Travel Distance) - for tau_wait:")
    print(f"  Values: {L_travel * 1e6} um")
    print(f"  Physical meaning: Distance dislocation travels before pinning")
    print(f"  Used in: tau_wait = L_t / (rho_m * b * epsilon_dot)")
    print(f"  Scale: micrometers (um)")
    
    print("\n" + "=" * 60)
    print("CRITICAL: These are DIFFERENT length scales!")
    print("  L_c (nm) << L_t (um)  [typically 100-1000x smaller]")
    print("  They have different physical meanings!")
    print("  They are used in different equations!")
    print("=" * 60)
    
    # Check that L_c << L_t
    L_c_max = L_capture.max()
    L_t_min = L_travel.min()
    
    if L_c_max < L_t_min:
        print(f"\n[OK] Validation passed: L_c_max ({L_c_max*1e9:.1f} nm) < L_t_min ({L_t_min*1e6:.1f} um)")
    else:
        print(f"\n[WARNING] L_c_max ({L_c_max*1e9:.1f} nm) >= L_t_min ({L_t_min*1e6:.1f} um)")
        print("  This is unusual - typically L_c should be much smaller than L_t")
    
    # Get literature ranges
    (L_c_min_lit, L_c_max_lit), (L_t_min_lit, L_t_max_lit) = get_literature_values()
    
    print(f"\nLiterature ranges:")
    print(f"  L_c: {L_c_min_lit*1e9:.1f} - {L_c_max_lit*1e9:.1f} nm")
    print(f"  L_t: {L_t_min_lit*1e6:.1f} - {L_t_max_lit*1e6:.1f} um")
    
    # Check if our values are in reasonable ranges
    if (L_capture.min() >= L_c_min_lit) and (L_capture.max() <= L_c_max_lit):
        print(f"\n[OK] L_c values are within literature range")
    else:
        print(f"\n[WARNING] L_c values may be outside typical literature range")
    
    if (L_travel.min() >= L_t_min_lit) and (L_travel.max() <= L_t_max_lit):
        print(f"[OK] L_t values are within literature range")
    else:
        print(f"[WARNING] L_t values may be outside typical literature range")

def main():
    """Main function."""
    validate_length_scales()
    
    # Create a summary table
    print("\n" + "=" * 60)
    print("Length Scale Summary Table")
    print("=" * 60)
    
    df = pd.DataFrame({
        'L_c (nm)': L_capture * 1e9,
        'L_t (µm)': L_travel * 1e6
    })
    
    print("\nValues to be used in DSA analysis:")
    print(df.to_string(index=False))
    
    # Save to file
    import os
    os.makedirs("outputs/analysis", exist_ok=True)
    
    # Create separate DataFrames for L_c and L_t
    df_Lc = pd.DataFrame({
        'L_c_nm': L_capture * 1e9,
        'description': 'Capture radius (nm) - for tau_diff calculation'
    })
    
    df_Lt = pd.DataFrame({
        'L_t_um': L_travel * 1e6,
        'description': 'Travel distance (um) - for tau_wait calculation'
    })
    
    # Save both
    df_Lc.to_csv("outputs/analysis/length_scales_Lc.csv", index=False)
    df_Lt.to_csv("outputs/analysis/length_scales_Lt.csv", index=False)
    
    # Also create a combined summary
    summary_text = f"""Length Scales for DSA Analysis

L_c (Capture Radius) - for tau_diff = L_c^2 / D_eff:
  Values: {L_capture * 1e9} nm
  Physical meaning: Distance for solute capture by dislocation
  Scale: nanometers

L_t (Travel Distance) - for tau_wait = L_t / (rho_m * b * epsilon_dot):
  Values: {L_travel * 1e6} um
  Physical meaning: Distance dislocation travels before pinning
  Scale: micrometers

CRITICAL: These are DIFFERENT length scales with different physical meanings!
"""
    
    with open("outputs/analysis/length_scales_summary.txt", 'w') as f:
        f.write(summary_text)
    print("\n[OK] Length scales saved to outputs/analysis/length_scales.csv")

if __name__ == "__main__":
    main()

