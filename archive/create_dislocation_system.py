"""
Script to create Al-5wt%Mg system with an edge dislocation.
"""

import numpy as np

def create_edge_dislocation_system(a0=4.05, nx=40, ny=40, nz=20, Mg_atomic_percent=5.52):
    """
    Create FCC Al-Mg system with an edge dislocation.
    
    Uses Volterra dislocation model with Burgers vector b = [a0, 0, 0]
    Dislocation line along z-axis.
    
    Parameters:
    -----------
    a0 : float
        Lattice constant (Angstrom)
    nx, ny, nz : int
        Number of unit cells in each direction
    Mg_atomic_percent : float
        Atomic percent of Mg
    
    Returns:
    --------
    positions : array
        Atomic positions (N, 3)
    types : array
        Atom types (1=Al, 2=Mg)
    box : array
        Box dimensions
    """
    # FCC basis
    basis = np.array([
        [0.0, 0.0, 0.0],
        [0.5, 0.5, 0.0],
        [0.5, 0.0, 0.5],
        [0.0, 0.5, 0.5]
    ])
    
    positions = []
    
    # Center of dislocation (in middle of x-y plane)
    x0 = nx * a0 / 2.0
    y0 = ny * a0 / 2.0
    
    # Burgers vector magnitude
    b = a0
    
    # Generate lattice with dislocation displacement field
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                for b_vec in basis:
                    x = (i + b_vec[0]) * a0
                    y = (j + b_vec[1]) * a0
                    z = (k + b_vec[2]) * a0
                    
                    # Displacement field for edge dislocation
                    # u_x = (b/(2π)) * [atan(y/x) + xy/(2(1-ν)(x²+y²))]
                    # Simplified: u_x = (b/(2π)) * atan(y/x)
                    dx = x - x0
                    dy = y - y0
                    
                    if abs(dx) < 1e-6 and abs(dy) < 1e-6:
                        # At core, use small offset
                        dx = 0.1 * a0
                    
                    # Displacement in x-direction
                    theta = np.arctan2(dy, dx)
                    ux = (b / (2 * np.pi)) * theta
                    
                    # Add displacement
                    x_displaced = x + ux
                    y_displaced = y
                    z_displaced = z
                    
                    positions.append([x_displaced, y_displaced, z_displaced])
    
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
    
    # Box dimensions (with padding for dislocation)
    box = np.array([
        [0.0, nx * a0 * 1.1],
        [0.0, ny * a0 * 1.1],
        [0.0, nz * a0]
    ])
    
    return positions, atom_types, box, (x0, y0)

def write_lammps_data(filename, positions, types, box):
    """Write LAMMPS data file."""
    n_atoms = len(positions)
    
    with open(filename, 'w') as f:
        f.write("# Al-5wt%Mg system with edge dislocation\n\n")
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
    import os
    
    os.makedirs("inputs/dislocation", exist_ok=True)
    
    positions, types, box, core_pos = create_edge_dislocation_system()
    
    write_lammps_data("inputs/dislocation/dislocation_system.data", positions, types, box)
    
    print(f"Created dislocation system with {len(positions)} atoms")
    print(f"Box size: {box[0,1]:.2f} x {box[1,1]:.2f} x {box[2,1]:.2f} Angstrom")
    print(f"Dislocation core at: ({core_pos[0]:.2f}, {core_pos[1]:.2f}) Angstrom")


