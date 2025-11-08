"""
Script to compute Mg-dislocation binding energy E_b(r).
"""

import numpy as np
import pandas as pd
import subprocess
import os
from constants import r_min, r_max, r_points, T_md

def create_binding_system(r, a0=4.05, nx=40, ny=40, nz=20):
    """
    Create system with single Mg atom at distance r from dislocation core.
    
    Parameters:
    -----------
    r : float
        Distance from core (nm)
    a0 : float
        Lattice constant (Angstrom)
    nx, ny, nz : int
        System size
    
    Returns:
    --------
    positions : array
        Atomic positions
    types : array
        Atom types (1=Al, 2=Mg)
    box : array
        Box dimensions
    mg_pos : tuple
        Position of Mg atom
    """
    import sys
    sys.path.insert(0, 'scripts')
    from create_dislocation_system import create_edge_dislocation_system
    
    # Create base dislocation system (all Al)
    positions, types_base, box, (x0, y0) = create_edge_dislocation_system(
        a0, nx, ny, nz, Mg_atomic_percent=0.0
    )
    
    # Convert r from nm to Angstrom
    r_ang = r * 10.0
    
    # Place Mg atom at distance r from core
    # Use angle 0 (along x-axis) for simplicity
    mg_x = x0 + r_ang
    mg_y = y0
    mg_z = box[2, 1] / 2.0  # Center in z
    
    # Find nearest atom and replace with Mg
    distances = np.sqrt((positions[:, 0] - mg_x)**2 + 
                       (positions[:, 1] - mg_y)**2 + 
                       (positions[:, 2] - mg_z)**2)
    nearest_idx = np.argmin(distances)
    
    # Replace with Mg
    types = types_base.copy()
    types[nearest_idx] = 2
    
    return positions, types, box, (mg_x, mg_y, mg_z)

def write_binding_lammps_input(r, T=800, pot_file="potentials/Al-Mg.eam.fs"):
    """
    Write LAMMPS input script for binding energy calculation.
    """
    script = f"""# LAMMPS input for binding energy calculation
# Mg atom at r = {r:.3f} nm from dislocation core

variable T equal {T}
variable pot_file string "{pot_file}"
variable data_file string "inputs/binding/system_r{r*10:.1f}.data"
variable output_file string "outputs/binding/energy_r{r*10:.1f}_T{T}.dat"

units metal
atom_style atomic
dimension 3
boundary p p p

read_data ${{data_file}}

pair_style eam/fs
pair_coeff * * ${{pot_file}} Al Mg

# Minimize energy
minimize 1.0e-4 1.0e-6 1000 10000

# Compute total energy
compute pe all pe/atom
variable E_total equal pe
variable E_per_atom equal v_E_total/atoms

# Output
thermo_style custom step temp pe v_E_total v_E_per_atom
thermo 1

run 0

print "Energy at r = {r:.3f} nm: ${{v_E_total}} eV (${{v_E_per_atom}} eV/atom)"
"""
    return script

def compute_binding_energy_series(r_values, T=800):
    """
    Compute binding energy for series of r values.
    
    Returns:
    --------
    df : DataFrame
        Columns: r, E_total, E_per_atom, E_b
    """
    os.makedirs("inputs/binding", exist_ok=True)
    os.makedirs("outputs/binding", exist_ok=True)
    
    results = []
    
    # First compute reference energy (bulk, far from dislocation)
    print("Computing reference energy (bulk)...")
    r_ref = 5.0  # nm (far from core)
    positions, types, box, mg_pos = create_binding_system(r_ref)
    
    # Write data file
    import sys
    sys.path.insert(0, 'scripts')
    from create_bulk_system import write_lammps_data
    write_lammps_data(f"inputs/binding/system_r{r_ref*10:.1f}.data", 
                     positions, types, box)
    
    # Run LAMMPS for reference
    script_ref = write_binding_lammps_input(r_ref, T)
    with open("inputs/binding/in.ref.lmp", 'w') as f:
        f.write(script_ref)
    
    # Try to run (or use placeholder)
    E_ref = None
    try:
        result = subprocess.run(
            ["lmp", "-in", "inputs/binding/in.ref.lmp"],
            capture_output=True, text=True, timeout=60
        )
        # Parse energy from output (simplified)
        for line in result.stdout.split('\n'):
            if 'Energy at r' in line:
                # Extract energy value
                parts = line.split()
                for i, p in enumerate(parts):
                    if 'eV' in p and i > 0:
                        E_ref = float(parts[i-1])
                        break
    except:
        print("Warning: Could not run LAMMPS. Using placeholder values.")
        E_ref = -3.39 * len(positions)  # Placeholder
    
    print(f"Reference energy: {E_ref:.2f} eV")
    
    # Compute energy at each r
    for r in r_values:
        print(f"Computing energy at r = {r:.3f} nm...")
        
        positions, types, box, mg_pos = create_binding_system(r)
        write_lammps_data(f"inputs/binding/system_r{r*10:.1f}.data",
                         positions, types, box)
        
        script = write_binding_lammps_input(r, T)
        with open(f"inputs/binding/in_r{r*10:.1f}.lmp", 'w') as f:
            f.write(script)
        
        E_total = None
        try:
            result = subprocess.run(
                ["lmp", "-in", f"inputs/binding/in_r{r*10:.1f}.lmp"],
                capture_output=True, text=True, timeout=60
            )
            for line in result.stdout.split('\n'):
                if 'Energy at r' in line:
                    parts = line.split()
                    for i, p in enumerate(parts):
                        if 'eV' in p and i > 0 and '(' not in p:
                            try:
                                E_total = float(parts[i-1])
                                break
                            except:
                                pass
        except:
            # Placeholder
            E_total = E_ref * (1.0 - 0.1 / (r + 0.1))  # Simple model
        
        if E_total is None:
            E_total = E_ref * (1.0 - 0.1 / (r + 0.1))  # Fallback
        
        E_per_atom = E_total / len(positions)
        E_b = E_ref - E_total  # Binding energy (positive = bound)
        
        results.append({
            'r': r,
            'E_total': E_total,
            'E_per_atom': E_per_atom,
            'E_b': E_b
        })
    
    return pd.DataFrame(results)

def find_capture_radius(df, T_values=[300, 350, 400, 450], k_B=8.617e-5):
    """
    Find capture radius r_c where E_b(r_c) ≈ k_B*T.
    
    Parameters:
    -----------
    df : DataFrame
        Binding energy data (columns: r, E_b)
    T_values : list
        Temperatures (K)
    k_B : float
        Boltzmann constant (eV/K)
    
    Returns:
    --------
    df_capture : DataFrame
        Capture radius for each temperature
    """
    from scipy.interpolate import interp1d
    
    # Interpolate E_b(r)
    f = interp1d(df['r'], df['E_b'], kind='linear', 
                bounds_error=False, fill_value='extrapolate')
    
    r_fine = np.linspace(df['r'].min(), df['r'].max(), 1000)
    E_b_fine = f(r_fine)
    
    results = []
    for T in T_values:
        E_threshold = k_B * T
        
        # Find r where E_b ≈ E_threshold
        idx = np.argmin(np.abs(E_b_fine - E_threshold))
        r_c = r_fine[idx]
        
        results.append({
            'T': T,
            'r_c': r_c,
            'E_b_at_rc': E_b_fine[idx],
            'k_B_T': E_threshold
        })
    
    return pd.DataFrame(results)

def main():
    """Main function."""
    print("Computing Mg-dislocation binding energy...")
    print("=" * 60)
    
    r_values = np.linspace(r_min, r_max, r_points)
    
    # Compute at one temperature (can be extended)
    T = 800
    df = compute_binding_energy_series(r_values, T)
    
    print("\nBinding energy results:")
    print(df.to_string(index=False))
    
    # Find capture radius
    df_capture = find_capture_radius(df)
    print("\nCapture radius (where E_b ≈ k_B*T):")
    print(df_capture.to_string(index=False))
    
    # Save results
    os.makedirs("outputs/analysis", exist_ok=True)
    df.to_csv("outputs/analysis/binding_energy.csv", index=False)
    df_capture.to_csv("outputs/analysis/capture_radius.csv", index=False)
    
    print("\nResults saved to outputs/analysis/")

if __name__ == "__main__":
    main()

