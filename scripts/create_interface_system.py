"""
Script to create an Al/Mg layered interface system for LAMMPS.
The structure consists of an FCC Al substrate with a Mg-rich overlayer.
"""

import numpy as np
import os
import argparse


def create_interface_system(a0=4.05, nx=6, ny=6, nz_al=12, nz_mg=4):
    """
    Create an FCC slab where the bottom region is Al and the top region is Mg.

    Parameters
    ----------
    a0 : float
        Lattice constant in Angstrom. We adopt the Al value to maintain a coherent interface.
    nx, ny : int
        Number of FCC unit cells along x and y directions.
    nz_al : int
        Number of FCC unit cells along z occupied by Al.
    nz_mg : int
        Number of FCC unit cells along z occupied by Mg.

    Returns
    -------
    positions : ndarray
        Atomic positions (N, 3) in Angstrom.
    types : ndarray
        Atom types (1 = Al, 2 = Mg).
    box : ndarray
        Simulation box bounds [[xlo, xhi], [ylo, yhi], [zlo, zhi]].
    """
    basis = np.array([
        [0.0, 0.0, 0.0],
        [0.5, 0.5, 0.0],
        [0.5, 0.0, 0.5],
        [0.0, 0.5, 0.5],
    ])

    nz_total = nz_al + nz_mg

    positions = []
    types = []

    for i in range(nx):
        for j in range(ny):
            for k in range(nz_total):
                for b in basis:
                    x = (i + b[0]) * a0
                    y = (j + b[1]) * a0
                    z = (k + b[2]) * a0
                    positions.append([x, y, z])

                    # Assign atom type based on z-layer
                    atom_type = 1 if k < nz_al else 2
                    types.append(atom_type)

    positions = np.array(positions)
    types = np.array(types, dtype=int)

    box = np.array([
        [0.0, nx * a0],
        [0.0, ny * a0],
        [0.0, nz_total * a0],
    ])

    return positions, types, box


def write_lammps_data(filename, positions, types, box):
    """
    Write LAMMPS data file for the interface system.
    """
    n_atoms = len(positions)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w") as f:
        f.write("# Al/Mg layered interface system\n\n")
        f.write(f"{n_atoms} atoms\n")
        f.write("3 atom types\n\n")

        f.write(f"{box[0, 0]:.6f} {box[0, 1]:.6f} xlo xhi\n")
        f.write(f"{box[1, 0]:.6f} {box[1, 1]:.6f} ylo yhi\n")
        f.write(f"{box[2, 0]:.6f} {box[2, 1]:.6f} zlo zhi\n\n")

        f.write("Masses\n\n")
        f.write("1 26.98  # Al\n")
        f.write("2 24.31  # Mg\n")
        f.write("3 65.38  # Zn (unused placeholder)\n\n")

        f.write("Atoms\n\n")
        for i, (pos, atype) in enumerate(zip(positions, types), start=1):
            f.write(f"{i} {atype} {pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f}\n")


def parse_args():
    parser = argparse.ArgumentParser(description="Build Al/Mg interface data file.")
    parser.add_argument("--a0", type=float, default=4.05, help="Lattice parameter (Å)")
    parser.add_argument("--nx", type=int, default=6, help="Number of FCC cells along x")
    parser.add_argument("--ny", type=int, default=6, help="Number of FCC cells along y")
    parser.add_argument("--nz-al", type=int, default=12, help="Number of FCC cells of Al along z")
    parser.add_argument("--nz-mg", type=int, default=4, help="Number of FCC cells of Mg along z")
    parser.add_argument(
        "--output",
        type=str,
        default="inputs/interface/interface_system.data",
        help="LAMMPS data output path",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    positions, types, box = create_interface_system(
        a0=args.a0, nx=args.nx, ny=args.ny, nz_al=args.nz_al, nz_mg=args.nz_mg
    )
    write_lammps_data(args.output, positions, types, box)

    n_atoms = len(positions)
    n_al = np.sum(types == 1)
    n_mg = np.sum(types == 2)
    print(f"Created interface structure at {args.output}")
    print(f"Total atoms: {n_atoms} (Al: {n_al}, Mg: {n_mg})")
    print(f"Box dimensions: {box[0,1]:.2f} x {box[1,1]:.2f} x {box[2,1]:.2f} Å")

