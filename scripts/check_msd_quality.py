"""
Quick script to check MSD data quality for bulk or interface runs.
"""

import argparse
import glob
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_msd_file(filename: Path):
    """
    Load an MSD file and determine its schema (bulk vs interface).
    """
    df = pd.read_csv(filename, sep=r"\s+", comment="#", header=None)

    if df.shape[1] == 5:
        df.columns = ["step", "msd_x", "msd_y", "msd_z", "msd_total"]
        schema = "bulk"
    elif df.shape[1] >= 9:
        df = df.iloc[:, :9]
        df.columns = [
            "step",
            "Mg_x",
            "Mg_y",
            "Mg_z",
            "Mg_total",
            "Al_x",
            "Al_y",
            "Al_z",
            "Al_total",
        ]
        schema = "interface"
    else:
        raise ValueError(
            f"Unexpected number of columns ({df.shape[1]}) in {filename}"
        )

    return df, schema


def analyze_component(time_ps, msd_ang, start_fraction=0.2):
    """
    Fit MSD vs time for a single component.
    """
    if np.all(np.isnan(msd_ang)):
        return None

    time_ps = np.asarray(time_ps)
    msd_ang = np.asarray(msd_ang)

    n = len(time_ps)
    start_idx = int(n * start_fraction)
    time_ps = time_ps[start_idx:]
    msd_ang = msd_ang[start_idx:]

    if len(time_ps) < 5:
        return None

    time_s = time_ps * 1e-12
    msd_m2 = msd_ang * 1e-20

    slope, intercept, r_value, p_value, std_err = stats.linregress(
        time_s, msd_m2
    )
    r2 = r_value**2
    D = slope / 2.0  # 1D Einstein relation

    return {
        "points": len(time_s),
        "r2": r2,
        "slope_ang2_per_ns": slope * 1e12,
        "D_m2_s": D,
        "std_err_m2_s": std_err / 2.0,
    }


def check_msd_file(filename, species=("Mg", "Al"), component="z"):
    """
    Perform quality checks for a given MSD file.
    """
    try:
        df, schema = load_msd_file(filename)
    except Exception as exc:
        print(f"\nFile: {filename}")
        print(f"  Error: {exc}")
        return

    time_ps = (df["step"] - df["step"].iloc[0]) * 0.001
    time_ns = time_ps / 1000.0

    print(f"\nFile: {filename}")
    print("=" * 70)
    print(f"Records: {len(df)}")
    print(f"Time window: {time_ns.iloc[0]:.3f} - {time_ns.iloc[-1]:.3f} ns")

    if schema == "bulk":
        print("Detected schema: bulk (single species MSD).")
        results = analyze_component(time_ps, df["msd_total"])
        if results:
            print(
                f"  R² = {results['r2']:.4f}, "
                f"D ≈ {results['D_m2_s']:.3e} m²/s "
                f"({results['points']} points)"
            )
        return

    print("Detected schema: interface (Mg & Al columns).")
    for sp in species:
        column = f"{sp}_{component}"
        if column not in df.columns:
            print(f"  {sp}: column {column} missing, skipping.")
            continue

        stats_dict = analyze_component(time_ps, df[column])
        if not stats_dict:
            print(f"  {sp}: insufficient data after transient cut.")
            continue

        trend = (
            "OK"
            if stats_dict["r2"] >= 0.95
            else ("WARN" if stats_dict["r2"] >= 0.8 else "POOR")
        )
        print(
            f"  {sp}: R^2={stats_dict['r2']:.4f} ({trend}), "
            f"D ~ {stats_dict['D_m2_s']:.3e} m^2/s, "
            f"points={stats_dict['points']}"
        )


def main():
    parser = argparse.ArgumentParser(description="Check MSD data quality.")
    parser.add_argument(
        "--pattern",
        default="outputs/interface_1k/msd_interface_T*.dat",
        help="Glob pattern for MSD files to check.",
    )
    parser.add_argument(
        "--species",
        nargs="+",
        default=["Mg", "Al"],
        help="Species to analyze (for interface schema).",
    )
    parser.add_argument(
        "--component",
        default="z",
        choices=["x", "y", "z", "total"],
        help="MSD component to analyze.",
    )
    parser.add_argument(
        "--start-fraction",
        type=float,
        default=0.2,
        help="Fraction of initial data to discard before fitting.",
    )

    args = parser.parse_args()

    files = sorted(glob.glob(args.pattern))
    if not files:
        print(f"No MSD files found for pattern: {args.pattern}")
        return

    print("Checking MSD Data Quality")
    print("=" * 70)
    for filename in files:
        check_msd_file(filename, species=args.species, component=args.component)


if __name__ == "__main__":
    main()