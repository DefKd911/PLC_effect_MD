"""
Updated DSA analysis script per professor feedback.
Uses two separate L values and analytical pipe diffusion.
"""

import argparse
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import (  # noqa: E402
    L_capture,
    L_travel,
    T_dsa,
    b,
    epsilon_dot,
    f_pipe,
    rho_m_values,
)

def compute_tau_diff(L_c, D_eff):
    """
    Compute diffusion time: τ_diff = L_c² / D_eff
    
    Parameters:
    -----------
    L_c : float or array
        Capture radius (m) - nm scale
    D_eff : float or array
        Effective diffusivity (m²/s) = D_bulk * (1 + f_pipe)
    
    Returns:
    --------
    tau_diff : float or array
        Diffusion time (s)
    """
    return (L_c ** 2) / D_eff

def compute_tau_wait(L_t, rho_m, b, epsilon_dot):
    """
    Compute waiting time: τ_wait = L_t / (ρ_m * b * ε̇)
    
    Parameters:
    -----------
    L_t : float or array
        Travel distance (m) - µm scale (NOT capture radius!)
    rho_m : float or array
        Mobile dislocation density (m⁻²)
    b : float
        Burgers vector (m)
    epsilon_dot : float
        Strain rate (s⁻¹)
    
    Returns:
    --------
    tau_wait : float or array
        Waiting time (s)
    """
    return L_t / (rho_m * b * epsilon_dot)

def normalize_diffusivity_df(df):
    """
    Ensure dataframe has columns ['T', 'D'].
    Accepts files with 'D', 'D_bulk', or 'D_interdiff'.
    """
    df = df.copy()
    if "D" in df.columns:
        pass
    elif "D_bulk" in df.columns:
        df = df.rename(columns={"D_bulk": "D"})
    elif "D_interdiff" in df.columns:
        df = df.rename(columns={"D_interdiff": "D"})
    else:
        raise KeyError(
            "Diffusivity column not found. Expected 'D', 'D_bulk', or 'D_interdiff'."
        )
    if "T" not in df.columns:
        raise KeyError("Temperature column 'T' is required.")
    return df[["T", "D"]].dropna()


def analyze_dsa_condition(D_bulk_df, pipe_factor):
    """
    Analyze DSA condition using MD-derived bulk diffusivity.
    Updated per professor feedback: uses two separate L values and analytical pipe diffusion.
    
    Parameters:
    -----------
    D_bulk_df : DataFrame
        Bulk diffusivity from MD (columns: T, D)
    
    Returns:
    --------
    results : dict
        Dictionary with (rho_m, L_c, L_t) as key, containing DataFrame with:
        T, D_bulk, D_eff, tau_diff, tau_wait, ratio
    """
    results = {}
    
    # Interpolate diffusivity to DSA temperature range
    try:
        from scipy.interpolate import interp1d
    except ImportError:
        print("Error: scipy not installed. Please install: pip install scipy")
        return {}
    
    f_D_bulk = interp1d(
        D_bulk_df["T"],
        D_bulk_df["D"],
        kind="linear",
        bounds_error=False,
        fill_value="extrapolate",
    )
    
    # Apply pipe diffusion correction: D_eff = D_bulk * (1 + f_pipe)
    
    for rho_m in rho_m_values:
        for L_c in L_capture:
            for L_t in L_travel:
                data = []
                
                for T in T_dsa:
                    # Get bulk diffusivity at this temperature
                    D_bulk = float(f_D_bulk(T))  # m²/s
                    
                    # Apply pipe diffusion correction
                    D_eff = D_bulk * (1.0 + pipe_factor)  # Effective diffusivity
                    
                    # Compute timescales with CORRECT L values
                    tau_diff = compute_tau_diff(L_c, D_eff)  # Uses L_c (capture radius)
                    tau_wait = compute_tau_wait(L_t, rho_m, b, epsilon_dot)  # Uses L_t (travel distance)
                    
                    # Ratio
                    ratio = tau_diff / tau_wait
                    
                    data.append({
                        "T": T,
                        "D_bulk": D_bulk,
                        "D_eff": D_eff,
                        "tau_diff": tau_diff,
                        "tau_wait": tau_wait,
                        "ratio": ratio,
                    })
                
                key = (rho_m, L_c, L_t)
                results[key] = pd.DataFrame(data)
    
    return results

def plot_dsa_analysis(results, output_file="outputs/analysis/tau_comparison.png"):
    """
    Plot τ_diff vs τ_wait for different parameter combinations.
    """
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Select a representative combination for main plot
    # Use middle values: rho_m=1e13, L_c=2nm, L_t=1µm
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: τ_diff and τ_wait vs T
    ax1 = axes[0]
    
    colors = ['blue', 'green', 'red']
    for i, ((rho_m, L_c, L_t), df) in enumerate(list(results.items())[:3]):
        label = f"ρ_m={rho_m:.0e}, L_c={L_c*1e9:.0f}nm, L_t={L_t*1e6:.1f}µm"
        ax1.loglog(df['T'], df['tau_diff'], '--', color=colors[i], 
                  linewidth=2, label=f'τ_diff ({label})')
        ax1.loglog(df['T'], df['tau_wait'], '-', color=colors[i], 
                  linewidth=2, label=f'τ_wait ({label})')
    
    ax1.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, label='τ_diff = τ_wait')
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Time (s)')
    ax1.set_title('Diffusion Time vs Waiting Time\n(Updated: Two L values)')
    ax1.legend(loc='best', fontsize=7)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Ratio τ_diff / τ_wait vs T
    ax2 = axes[1]
    
    for i, ((rho_m, L_c, L_t), df) in enumerate(list(results.items())[:3]):
        label = f"ρ_m={rho_m:.0e}, L_c={L_c*1e9:.0f}nm, L_t={L_t*1e6:.1f}µm"
        ax2.semilogy(df['T'], df['ratio'], '-', color=colors[i], 
                    linewidth=2, label=label, marker='o', markersize=4)
    
    ax2.axhline(y=1.0, color='black', linestyle=':', alpha=0.5, 
               label='DSA condition (τ_diff = τ_wait)')
    ax2.axhspan(0.1, 10.0, alpha=0.2, color='yellow', 
               label='DSA regime (0.1 < ratio < 10)')
    ax2.set_xlabel('Temperature (K)')
    ax2.set_ylabel('τ_diff / τ_wait')
    ax2.set_title('DSA Condition: τ_diff / τ_wait')
    ax2.legend(loc='best', fontsize=7)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"DSA analysis plot saved to {output_file}")
    plt.close()

def main():
    """Main function - Updated per professor feedback."""
    print("Analyzing DSA conditions (Updated workflow)...")
    print("=" * 60)
    
    # Load data
    parser = argparse.ArgumentParser(
        description="Analyze DSA/PLC conditions using diffusivity data."
    )
    parser.add_argument(
        "--input",
        default="outputs/analysis/arrhenius_interface_interdiff_extrapolated.csv",
        help="CSV file with columns T and D (or D_bulk/D_interdiff).",
    )
    parser.add_argument(
        "--pipe-factor",
        type=float,
        default=f_pipe,
        help="Pipe diffusion correction factor (D_eff = D*(1 + factor)).",
    )
    parser.add_argument(
        "--output",
        default="outputs/analysis",
        help="Directory to store analysis results.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        df_input = pd.read_csv(args.input)
    except FileNotFoundError:
        print(f"Error: Diffusivity data file not found: {args.input}")
        print("Run fit_arrhenius.py to generate extrapolated diffusivities.")
        return

    df_input = normalize_diffusivity_df(df_input)

    results = analyze_dsa_condition(df_input, args.pipe_factor)
    
    # Plot and save results
    import os
    os.makedirs("outputs/analysis", exist_ok=True)
    
    print("\nDSA Analysis Results:")
    print("-" * 60)
    
    for (rho_m, L_c, L_t), df in results.items():
        # Identify DSA regimes
        in_regime = (df['ratio'] > 0.1) & (df['ratio'] < 10.0)
        
        if in_regime.any():
            T_range = df[in_regime]['T']
            print(
                f"rho_m={rho_m:.0e} m^-2, L_c={L_c*1e9:.1f} nm, "
                f"L_t={L_t*1e6:.1f} um:"
            )
            print(f"  DSA possible: {T_range.min():.0f} - {T_range.max():.0f} K")
        
        # Save results
        filename = output_dir / f"dsa_rho{rho_m:.0e}_Lc{L_c*1e9:.0f}nm_Lt{L_t*1e6:.1f}um.csv"
        df.to_csv(filename, index=False)
    
    # Plot
    plot_path = output_dir / "tau_comparison.png"
    plot_dsa_analysis(results, output_file=str(plot_path))
    
    print(f"\nResults saved to {output_dir}/")

if __name__ == "__main__":
    main()

