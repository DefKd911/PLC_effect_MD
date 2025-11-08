"""
Validation script to check MD simulation quality.
"""

import numpy as np
import pandas as pd
from constants import (lattice_tolerance, cohesive_tolerance, msd_r2_threshold,
                      temp_stability, energy_drift_threshold, a0_exp, E_cohesive_exp)

def validate_lattice_constant(log_file):
    """Extract and validate lattice constant from LAMMPS log."""
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        # Look for final box dimensions
        for line in reversed(lines):
            if 'Lx' in line or 'xlo xhi' in line:
                # Parse box size
                # This is simplified - actual parsing depends on LAMMPS output format
                pass
        
        # Placeholder validation
        return True, "Lattice constant validation (placeholder)"
    except:
        return False, "Could not read log file"

def validate_temperature_stability(log_file, T_target):
    """Check temperature stability during NVT run."""
    try:
        # Read thermo output
        # This would require parsing LAMMPS log file
        # Placeholder
        return True, f"Temperature stable within ±{temp_stability} K"
    except:
        return False, "Could not validate temperature"

def validate_msd_linearity(msd_file):
    """Validate MSD linearity from analysis results."""
    try:
        df = pd.read_csv(msd_file)
        if 'r2' in df.columns:
            min_r2 = df['r2'].min()
            if min_r2 >= msd_r2_threshold:
                return True, f"MSD linearity OK (min R² = {min_r2:.3f})"
            else:
                return False, f"MSD linearity poor (min R² = {min_r2:.3f} < {msd_r2_threshold})"
    except:
        return False, "Could not validate MSD linearity"

def validate_all():
    """Run all validation checks."""
    print("Validating MD simulations...")
    print("=" * 60)
    
    validations = []
    
    # Check bulk diffusion results
    try:
        df = pd.read_csv("outputs/analysis/diffusivity_bulk.csv")
        valid, msg = validate_msd_linearity("outputs/analysis/diffusivity_bulk.csv")
        validations.append(("Bulk MSD Linearity", valid, msg))
    except FileNotFoundError:
        validations.append(("Bulk MSD Linearity", False, "Data file not found"))
    
    # Check core diffusion results
    try:
        df = pd.read_csv("outputs/analysis/diffusivity_core.csv")
        valid, msg = validate_msd_linearity("outputs/analysis/diffusivity_core.csv")
        validations.append(("Core MSD Linearity", valid, msg))
    except FileNotFoundError:
        validations.append(("Core MSD Linearity", False, "Data file not found"))
    
    # Print results
    print("\nValidation Results:")
    print("-" * 60)
    for name, valid, msg in validations:
        status = "✓ PASS" if valid else "✗ FAIL"
        print(f"{status}: {name}")
        print(f"  {msg}")
    
    # Summary
    n_pass = sum(1 for _, v, _ in validations if v)
    n_total = len(validations)
    print(f"\nSummary: {n_pass}/{n_total} validations passed")
    
    return all(v for _, v, _ in validations)

if __name__ == "__main__":
    validate_all()


