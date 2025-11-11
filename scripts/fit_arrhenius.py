"""
Script to fit Arrhenius equation to diffusivity data.
D = D₀ * exp(-Q / (R*T))
"""

import argparse
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from constants import R, T_dsa  # noqa: E402

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

def fit_arrhenius(df, D_col, weight_col=None):
    """
    Fit Arrhenius equation to diffusivity data.
    
    Parameters
    ----------
    df : DataFrame with columns ['T', D_col] and optional weight_col
    D_col : str
        Column name containing diffusivities (m²/s)
    weight_col : str or None
        Column name with weights/quality metric (e.g., R²). Rows with NaN are ignored.
    """
    if "T" not in df.columns:
        raise KeyError("Input dataframe must contain a 'T' column (temperature in K).")

    df_valid = df.dropna(subset=["T", D_col]).copy()
    if weight_col and weight_col in df_valid.columns:
        df_valid = df_valid.dropna(subset=[weight_col])

    if len(df_valid) < 3:
        raise ValueError("Need at least 3 data points for Arrhenius fit.")

    T = df_valid["T"].values
    D = df_valid[D_col].values
    log_D = np.log(D)
    inv_T = 1.0 / T

    coeffs = np.polyfit(inv_T, log_D, 1)
    slope, intercept = coeffs
    Q = -slope * R
    D0 = np.exp(intercept)

    # Estimate uncertainties from covariance of linear fit
    _, cov = np.polyfit(inv_T, log_D, 1, cov=True)
    slope_err = np.sqrt(cov[0, 0])
    intercept_err = np.sqrt(cov[1, 1])
    Q_err = slope_err * R
    D0_err = D0 * intercept_err

    Q_eV = Q / 96485
    pcov = np.array([[D0_err**2, 0], [0, Q_err**2]])
    return D0, Q, Q_eV, (D0, Q), pcov, df_valid

def extrapolate_to_dsa_temps(D0, Q, T_extrap=T_dsa):
    """
    Extrapolate diffusivity to DSA temperature range.
    """
    D_extrap = arrhenius(T_extrap, D0, Q)
    return pd.DataFrame({'T': T_extrap, 'D': D_extrap})

def plot_arrhenius(df, D0, Q, Q_eV, D_col, label, output_file):
    """
    Plot Arrhenius fit.
    """
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df_fit = df.dropna(subset=["T", D_col]).copy()
    T_fit = np.linspace(df_fit["T"].min(), df_fit["T"].max(), 200)
    D_fit = arrhenius(T_fit, D0, Q)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(T_fit, D_fit, "r-", label=f"Fit: D₀={D0:.2e} m²/s, Q={Q_eV:.2f} eV")
    ax1.scatter(df_fit["T"], df_fit[D_col], c="blue", s=50, label="MD data", zorder=5)
    ax1.set_xlabel("Temperature (K)")
    ax1.set_ylabel("Diffusivity D (m²/s)")
    ax1.set_yscale("log")
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_title(f"Arrhenius Fit ({label})")

    inv_T_fit = 1.0 / T_fit
    ax2.plot(inv_T_fit * 1000, np.log(D_fit), "r-", label=f"Fit: Q={Q/1000:.1f} kJ/mol")
    ax2.scatter(1000 / df_fit["T"], np.log(df_fit[D_col]), c="blue", s=50, label="MD data")
    ax2.set_xlabel("1000/T (K⁻¹)")
    ax2.set_ylabel("ln(D) (m²/s)")
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_title(f"ln(D) vs 1/T ({label})")

    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"Arrhenius plot saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Fit an Arrhenius relation to diffusivity data."
    )
    parser.add_argument(
        "--input",
        default="outputs/analysis/interface_diffusivity_1k.csv",
        help="CSV file containing columns T and diffusivity values.",
    )
    parser.add_argument(
        "--species",
        default="interdiff",
        choices=["Mg", "Al", "interdiff"],
        help="Which diffusivity column to fit.",
    )
    parser.add_argument(
        "--r2-threshold",
        type=float,
        default=0.0,
        help="Minimum R² value to include a point (column must exist).",
    )
    parser.add_argument(
        "--output-prefix",
        default="outputs/analysis/arrhenius_interface",
        help="Prefix for output artefacts (plot, params, extrapolation).",
    )
    parser.add_argument(
        "--extrapolate",
        action="store_true",
        help="Also extrapolate diffusivity to T_dsa range.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    df = pd.read_csv(input_path)

    species = args.species
    if species == "interdiff":
        D_col = "D_interdiff"
        weight_col = None
    else:
        D_col = f"D_{species}"
        weight_col = f"R2_{species}"
        if args.r2_threshold > 0 and weight_col in df.columns:
            df = df[df[weight_col] >= args.r2_threshold]

    print("Fitting Arrhenius equation...")
    print("=" * 60)

    D0, Q, Q_eV, popt, pcov, df_fit = fit_arrhenius(df, D_col, weight_col)
    D0_err = np.sqrt(pcov[0, 0])
    Q_err = np.sqrt(pcov[1, 1])
    Q_eV_err = Q_err / 96485

    print("\nArrhenius Fit Results:")
    print(f"  D0 = ({D0:.3e} +/- {D0_err:.3e}) m^2/s")
    print(f"  Q  = ({Q/1e3:.2f} +/- {Q_err/1e3:.2f}) kJ/mol")
    print(f"  Q  = ({Q_eV:.3f} +/- {Q_eV_err:.3f}) eV/atom")

    prefix = Path(args.output_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)

    params_df = pd.DataFrame(
        {
            "parameter": ["D0", "Q_kJmol", "Q_eV"],
            "value": [D0, Q / 1e3, Q_eV],
            "error": [D0_err, Q_err / 1e3, Q_eV_err],
        }
    )
    params_path = prefix.parent / f"{prefix.name}_{species}_params.csv"
    params_df.to_csv(params_path, index=False)
    print(f"Parameters saved to {params_path}")

    plot_path = prefix.parent / f"{prefix.name}_{species}.png"
    plot_arrhenius(df_fit, D0, Q, Q_eV, D_col, species, plot_path)

    if args.extrapolate:
        df_extrap = extrapolate_to_dsa_temps(D0, Q)
        extrap_path = prefix.parent / f"{prefix.name}_{species}_extrapolated.csv"
        df_extrap.to_csv(extrap_path, index=False)
        print(f"Extrapolated diffusivities saved to {extrap_path}")

if __name__ == "__main__":
    main()


