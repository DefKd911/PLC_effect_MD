"""
Script to create initial Al-5wt%Mg bulk system for LAMMPS.
"""

import numpy as np

def create_bulk_system(a0=4.05, nx=6, ny=6, nz=6, Mg_atomic_percent=5.52):
    """
    Create FCC Al-Mg bulk system.
    
    Updated per professor advice:
    - System size: At least 1000 atoms (not too small, not too big for optimization)
    - 6×6×6 unit cells = 864 atoms (4 atoms per unit cell)
    - This balances the "at least 1000 atoms" requirement with optimization needs
    
    Parameters:
    -----------
    a0 : float
        Lattice constant (Angstrom)
    nx, ny, nz : int
        Number of unit cells in each direction (default 6×6×6 = 864 atoms)
    Mg_atomic_percent : float
        Atomic percent of Mg (default 5.52 at% for 5 wt%)
    
    Returns:
    --------
    positions : array
        Atomic positions (N, 3)
    types : array
        Atom types (1=Al, 2=Mg)
    box : array
        Box dimensions (3, 2) - [[xlo, xhi], [ylo, yhi], [zlo, zhi]]
    """
    # FCC basis vectors
    basis = np.array([
        [0.0, 0.0, 0.0],
        [0.5, 0.5, 0.0],
        [0.5, 0.0, 0.5],
        [0.0, 0.5, 0.5]
    ])
    
    positions = []
    types = []
    
    # Generate FCC lattice
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                for b in basis:
                    x = (i + b[0]) * a0
                    y = (j + b[1]) * a0
                    z = (k + b[2]) * a0
                    positions.append([x, y, z])
    
    positions = np.array(positions)
    n_atoms = len(positions)
    
    # Randomly assign Mg atoms
    n_Mg = int(n_atoms * Mg_atomic_percent / 100.0)
    n_Al = n_atoms - n_Mg
    
    atom_types = np.concatenate([
        np.ones(n_Al, dtype=int),
        np.ones(n_Mg, dtype=int) * 2
    ])
    np.random.shuffle(atom_types)
    
    # Box dimensions
    box = np.array([
        [0.0, nx * a0],
        [0.0, ny * a0],
        [0.0, nz * a0]
    ])
    
    return positions, atom_types, box

def write_lammps_data(filename, positions, types, box):
    """
    Write LAMMPS data file.
    """
    n_atoms = len(positions)
    
    with open(filename, 'w') as f:
        f.write("# Al-5wt%Mg bulk system\n\n")
        f.write(f"{n_atoms} atoms\n")
        f.write("2 atom types\n\n")
        f.write(f"{box[0,0]:.6f} {box[0,1]:.6f} xlo xhi\n")
        f.write(f"{box[1,0]:.6f} {box[1,1]:.6f} ylo yhi\n")
        f.write(f"{box[2,0]:.6f} {box[2,1]:.6f} zlo zhi\n\n")
        f.write("Masses\n\n")
        f.write("1 26.98  # Al\n")
        f.write("2 24.31  # Mg\n\n")
        f.write("Atoms\n\n")
        
        for i, (pos, atype) in enumerate(zip(positions, types), 1):
            f.write(f"{i} {atype} {pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f}\n")

if __name__ == "__main__":
    import sys
    import os
    
    # Create output directory
    os.makedirs("inputs/bulk", exist_ok=True)
    
    # Create system
    positions, types, box = create_bulk_system()
    
    # Write data file
    write_lammps_data("inputs/bulk/bulk_system.data", positions, types, box)
    print(f"Created bulk system with {len(positions)} atoms")
    print(f"Box size: {box[0,1]:.2f} x {box[1,1]:.2f} x {box[2,1]:.2f} Angstrom")


