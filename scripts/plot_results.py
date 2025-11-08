"""
Plotting utilities for all analysis results.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def plot_binding_energy(output_file="outputs/analysis/eb_vs_r.png"):
    """Plot binding energy vs distance from dislocation core."""
    try:
        df = pd.read_csv("outputs/analysis/binding_energy.csv")
    except FileNotFoundError:
        print("Binding energy data not found.")
        return
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.plot(df['r'], df['E_b'], 'b-o', linewidth=2, markersize=6)
    ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # Mark capture radius for different temperatures
    try:
        r_c_df = pd.read_csv("outputs/analysis/capture_radius.csv")
        for _, row in r_c_df.iterrows():
            ax.axvline(x=row['r_c'], color='red', linestyle=':', alpha=0.5,
                      label=f"r_c at T={row['T']:.0f} K" if _ == 0 else "")
            ax.plot(row['r_c'], row['E_b_at_rc'], 'ro', markersize=8)
    except:
        pass
    
    ax.set_xlabel('Distance from core r (nm)')
    ax.set_ylabel('Binding Energy E_b (eV)')
    ax.set_title('Mg-Dislocation Binding Energy')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Binding energy plot saved to {output_file}")
    plt.close()

def plot_radial_diffusivity(output_file="outputs/analysis/radial_diffusivity.png"):
    """Plot diffusivity vs radial distance from dislocation core."""
    try:
        df = pd.read_csv("outputs/analysis/diffusivity_radial.csv")
    except FileNotFoundError:
        print("Radial diffusivity data not found.")
        return
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Plot for each temperature
    for T in df['T'].unique():
        df_T = df[df['T'] == T]
        ax.semilogy(df_T['r'], df_T['D'], 'o-', label=f'T = {T:.0f} K', linewidth=2)
    
    # Add bulk diffusivity line for reference
    try:
        bulk_df = pd.read_csv("outputs/analysis/diffusivity_bulk.csv")
        bulk_df = bulk_df[bulk_df['valid'] == True]
        for T in bulk_df['T'].values:
            D_bulk = bulk_df[bulk_df['T'] == T]['D'].values[0]
            ax.axhline(y=D_bulk, linestyle='--', alpha=0.5, 
                      label=f'D_bulk at {T:.0f} K' if T == bulk_df['T'].iloc[0] else "")
    except:
        pass
    
    ax.set_xlabel('Distance from core r (nm)')
    ax.set_ylabel('Diffusivity D (m²/s)')
    ax.set_title('Pipe Diffusion: D vs Distance from Core')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Radial diffusivity plot saved to {output_file}")
    plt.close()

def plot_experimental_comparison(output_file="outputs/analysis/md_vs_experiment.png"):
    """Compare MD results with experimental data."""
    # Load MD data
    try:
        md_df = pd.read_csv("outputs/analysis/diffusivity_bulk.csv")
        md_df = md_df[md_df['valid'] == True]
    except FileNotFoundError:
        print("MD diffusivity data not found.")
        return
    
    # Load Arrhenius fit
    try:
        fit_params = pd.read_csv("outputs/analysis/arrhenius_params_bulk.csv")
        D0 = fit_params[fit_params['parameter'] == 'D0']['value'].values[0]
        Q_kJ = fit_params[fit_params['parameter'] == 'Q_kJmol']['value'].values[0]
        Q = Q_kJ * 1e3  # J/mol
    except:
        print("Arrhenius fit parameters not found.")
        return
    
    # Experimental data (literature values for Mg in Al)
    # These are approximate - user should replace with actual literature data
    T_exp = np.array([573, 623, 673, 723, 773, 823, 873])
    # Placeholder values - user should replace with actual experimental data
    D_exp = 1.0e-4 * np.exp(-130e3 / (8.314 * T_exp))  # Placeholder
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot 1: D vs T
    T_fit = np.linspace(md_df['T'].min(), md_df['T'].max(), 100)
    # Arrhenius equation: D = D0 * exp(-Q / (R*T))
    R = 8.314  # J/(mol·K)
    D_fit = D0 * np.exp(-Q / (R * T_fit))
    
    ax1.semilogy(T_fit, D_fit, 'r-', linewidth=2, label='MD Arrhenius fit')
    ax1.scatter(md_df['T'], md_df['D'], c='blue', s=50, zorder=5, label='MD data')
    ax1.scatter(T_exp, D_exp, c='green', s=50, marker='s', zorder=5, label='Experiment (placeholder)')
    
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Diffusivity D (m²/s)')
    ax1.set_title('MD vs Experimental Diffusivity')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: ln(D) vs 1/T
    ax2.plot(1000/T_fit, np.log(D_fit), 'r-', linewidth=2, label='MD Arrhenius fit')
    ax2.scatter(1000/md_df['T'], np.log(md_df['D']), c='blue', s=50, zorder=5, label='MD data')
    ax2.scatter(1000/T_exp, np.log(D_exp), c='green', s=50, marker='s', zorder=5, label='Experiment')
    
    ax2.set_xlabel('1000/T (K⁻¹)')
    ax2.set_ylabel('ln(D) (m²/s)')
    ax2.set_title('Arrhenius Plot: MD vs Experiment')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Experimental comparison plot saved to {output_file}")
    plt.close()
    
    # Compute deviation
    if len(T_exp) > 0:
        D_exp_interp = interp1d(T_exp, D_exp, kind='linear', 
                               bounds_error=False, fill_value='extrapolate')
        T_common = np.intersect1d(md_df['T'].values, T_exp)
        if len(T_common) > 0:
            D_md_common = md_df[md_df['T'].isin(T_common)]['D'].values
            D_exp_common = D_exp_interp(T_common)
            deviation = np.abs((D_md_common - D_exp_common) / D_exp_common) * 100
            print(f"\nAverage deviation from experiment: {deviation.mean():.1f}%")

def plot_all():
    """Generate all plots."""
    print("Generating all plots...")
    print("=" * 60)
    
    plot_binding_energy()
    plot_radial_diffusivity()
    plot_experimental_comparison()
    
    print("\nAll plots generated.")

if __name__ == "__main__":
    plot_all()

