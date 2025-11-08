"""
Script to fit Arrhenius equation to diffusivity data.
D = D₀ * exp(-Q / (R*T))
"""

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from constants import R, T_dsa

def arrhenius(T, D0, Q):
    """
    Arrhenius equation for diffusivity.
    
    Parameters:
    -----------
    T : array
        Temperature in K
    D0 : float
        Pre-exponential factor (m²/s)
    Q : float
        Activation energy (J/mol)
    
    Returns:
    --------
    D : array
        Diffusivity (m²/s)
    """
    return D0 * np.exp(-Q / (R * T))

def fit_arrhenius(df):
    """
    Fit Arrhenius equation to diffusivity data.
    
    Parameters:
    -----------
    df : DataFrame
        Must have columns: T, D, valid
    
    Returns:
    --------
    D0 : float
        Pre-exponential factor (m²/s)
    Q : float
        Activation energy (J/mol)
    Q_eV : float
        Activation energy (eV/atom)
    popt : array
        Fitted parameters [D0, Q]
    pcov : array
        Covariance matrix
    """
    # Filter valid data
    df_valid = df[df['valid'] == True].copy()
    
    if len(df_valid) < 3:
        raise ValueError("Need at least 3 valid data points for Arrhenius fit")
    
    T = df_valid['T'].values
    D = df_valid['D'].values
    
    # Use log space for better fit
    # ln(D) = ln(D0) - Q/(R*T)
    log_D = np.log(D)
    inv_T = 1.0 / T
    
    # Linear fit in log space
    coeffs = np.polyfit(inv_T, log_D, 1)
    Q_linear = -coeffs[0] * R  # J/mol
    log_D0_linear = coeffs[1]
    D0_linear = np.exp(log_D0_linear)
    
    # Use linear fit as initial guess for nonlinear fit
    p0 = [D0_linear, Q_linear]
    
    # Nonlinear fit with error weighting if available
    if 'D_err' in df_valid.columns:
        weights = 1.0 / (df_valid['D_err'].values + 1e-30)
        weights = weights / weights.max()
    else:
        weights = None
    
    try:
        popt, pcov = curve_fit(arrhenius, T, D, p0=p0, sigma=weights, 
                              absolute_sigma=False, maxfev=10000)
        D0, Q = popt
    except:
        # Fallback to linear fit
        D0, Q = D0_linear, Q_linear
        pcov = np.array([[D0*0.1, 0], [0, Q*0.1]])
    
    # Convert Q to eV/atom
    Q_eV = Q / (R * 1e3 / 4.184) / 6.022e23 * 1.602e-19  # J/mol -> eV/atom
    # Simplified: Q_eV ≈ Q / 96485 (rough conversion)
    Q_eV = Q / 96485  # More accurate: J/mol to eV/atom
    
    return D0, Q, Q_eV, popt, pcov

def extrapolate_to_dsa_temps(D0, Q, T_extrap=T_dsa):
    """
    Extrapolate diffusivity to DSA temperature range.
    """
    D_extrap = arrhenius(T_extrap, D0, Q)
    return pd.DataFrame({'T': T_extrap, 'D': D_extrap})

def plot_arrhenius(df, D0, Q, Q_eV, output_file="outputs/analysis/arrhenius_fit.png"):
    """
    Plot Arrhenius fit.
    """
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Filter valid data
    df_valid = df[df['valid'] == True].copy()
    df_invalid = df[df['valid'] == False].copy()
    
    # Plot 1: D vs T (linear scale)
    T_fit = np.linspace(df_valid['T'].min(), df_valid['T'].max(), 100)
    D_fit = arrhenius(T_fit, D0, Q)
    
    ax1.plot(T_fit, D_fit, 'r-', label=f'Fit: D₀={D0:.2e} m²/s, Q={Q_eV:.2f} eV')
    ax1.scatter(df_valid['T'], df_valid['D'], c='blue', s=50, 
               label='MD data (valid)', zorder=5)
    if len(df_invalid) > 0:
        ax1.scatter(df_invalid['T'], df_invalid['D'], c='red', s=50, 
                   marker='x', label='MD data (invalid)', zorder=5)
    
    ax1.set_xlabel('Temperature (K)')
    ax1.set_ylabel('Diffusivity D (m²/s)')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_title('Arrhenius Fit: D vs T')
    
    # Plot 2: ln(D) vs 1/T
    inv_T_fit = 1.0 / T_fit
    log_D_fit = np.log(D_fit)
    
    ax2.plot(inv_T_fit * 1000, log_D_fit, 'r-', 
            label=f'Fit: Q={Q_eV:.2f} eV, Q={Q/1e3:.1f} kJ/mol')
    ax2.scatter(1000/df_valid['T'], np.log(df_valid['D']), c='blue', s=50,
               label='MD data (valid)', zorder=5)
    if len(df_invalid) > 0:
        ax2.scatter(1000/df_invalid['T'], np.log(df_invalid['D']), c='red', s=50,
                   marker='x', label='MD data (invalid)', zorder=5)
    
    ax2.set_xlabel('1000/T (K⁻¹)')
    ax2.set_ylabel('ln(D) (m²/s)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_title('Arrhenius Fit: ln(D) vs 1/T')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Arrhenius plot saved to {output_file}")
    plt.close()

def main():
    """Main function."""
    import sys
    
    # Read diffusivity data
    try:
        df = pd.read_csv("outputs/analysis/diffusivity_bulk.csv")
    except FileNotFoundError:
        print("Error: diffusivity_bulk.csv not found. Run analyze_msd.py first.")
        sys.exit(1)
    
    print("Fitting Arrhenius equation...")
    print("=" * 60)
    
    try:
        D0, Q, Q_eV, popt, pcov = fit_arrhenius(df)
        
        # Calculate uncertainties
        D0_err = np.sqrt(pcov[0, 0])
        Q_err = np.sqrt(pcov[1, 1])
        Q_eV_err = Q_err / 96485
        
        print(f"\nArrhenius Fit Results:")
        print(f"  D₀ = ({D0:.4e} ± {D0_err:.4e}) m²/s")
        print(f"  Q  = ({Q/1e3:.2f} ± {Q_err/1e3:.2f}) kJ/mol")
        print(f"  Q  = ({Q_eV:.3f} ± {Q_eV_err:.3f}) eV/atom")
        
        # Extrapolate to DSA temperatures
        df_extrap = extrapolate_to_dsa_temps(D0, Q)
        df_extrap.to_csv("outputs/analysis/diffusivity_bulk_extrapolated.csv", index=False)
        print(f"\nExtrapolated to DSA temperature range (300-450 K)")
        print(f"  Saved to: outputs/analysis/diffusivity_bulk_extrapolated.csv")
        
        # Plot
        plot_arrhenius(df, D0, Q, Q_eV)
        
        # Save fit parameters
        fit_params = pd.DataFrame({
            'parameter': ['D0', 'Q_kJmol', 'Q_eV'],
            'value': [D0, Q/1e3, Q_eV],
            'error': [D0_err, Q_err/1e3, Q_eV_err]
        })
        fit_params.to_csv("outputs/analysis/arrhenius_params_bulk.csv", index=False)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()


