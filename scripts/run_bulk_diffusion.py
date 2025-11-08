"""
Script to run bulk diffusion simulations at multiple temperatures.
"""

import os
import subprocess
import sys
from constants import T_md

def run_lammps_script(script_path, log_path):
    """Run LAMMPS script and capture output."""
    try:
        # Check if LAMMPS is available
        result = subprocess.run(
            ["lmp", "-in", script_path, "-log", log_path],
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except FileNotFoundError:
        print("ERROR: LAMMPS executable 'lmp' not found in PATH")
        print("Please ensure LAMMPS is installed and 'lmp' is in your PATH")
        return False, "LAMMPS not found"

def create_bulk_input_for_T(T, pot_file="potentials/Al-Mg.eam.fs"):
    """Create LAMMPS input file for specific temperature."""
    script_content = f"""# LAMMPS input script for bulk Mg diffusion in Al-5wt%Mg
# Temperature: {T} K

variable T equal {T}
variable pot_file string "potentials/Al-Mg.eam.fs"
variable data_file string "inputs/bulk/bulk_system.data"
variable output_dir string "outputs/bulk"
variable dump_freq equal 1000
variable thermo_freq equal 100

units metal
atom_style atomic
dimension 3
boundary p p p

read_data ${{data_file}}

pair_style eam/fs
pair_coeff * * ${{pot_file}} Al Mg

compute msd_Mg all msd com yes
compute temp_Mg all temp/partial 0 0 1

reset_timestep 0
timestep 0.001

velocity all create ${{T}} {12345 + int(T)} rot yes dist gaussian

fix 1 all npt temp ${{T}} ${{T}} 0.1 iso 0.0 0.0 1.0
thermo_style custom step temp pe ke etotal press vol lx ly lz
thermo ${{thermo_freq}}
run 50000

unfix 1
fix 1 all nvt temp ${{T}} ${{T}} 0.1
fix 2 all ave/time 1 1 ${{dump_freq}} c_msd_Mg[1] c_msd_Mg[2] c_msd_Mg[3] c_msd_Mg[4] file ${{output_dir}}/msd_T{T}.dat

dump 1 all custom ${{dump_freq}} ${{output_dir}}/traj_T{T}.lammpstrj id type x y z
dump_modify 1 element Al Mg

thermo_style custom step temp pe ke etotal press vol c_temp_Mg
thermo ${{thermo_freq}}

run 10000000

print "Simulation completed at T = ${{T}} K"
"""
    return script_content

def main():
    """Main function to run all bulk diffusion simulations."""
    # Create necessary directories
    os.makedirs("outputs/bulk", exist_ok=True)
    os.makedirs("inputs/bulk", exist_ok=True)
    
    # Check if bulk system data file exists
    if not os.path.exists("inputs/bulk/bulk_system.data"):
        print("Creating bulk system...")
        sys.path.insert(0, 'scripts')
        from create_bulk_system import create_bulk_system, write_lammps_data
        positions, types, box = create_bulk_system()
        write_lammps_data("inputs/bulk/bulk_system.data", positions, types, box)
        print("Bulk system created.")
    
    print(f"Running bulk diffusion simulations at temperatures: {T_md} K")
    print("=" * 60)
    
    results = {}
    
    for T in T_md:
        print(f"\nRunning simulation at T = {T} K...")
        
        # Create input file for this temperature
        script_content = create_bulk_input_for_T(T)
        script_path = f"inputs/bulk/in.bulk_T{T}.lmp"
        log_path = f"outputs/bulk/log_T{T}.log"
        
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Run LAMMPS
        success, output = run_lammps_script(script_path, log_path)
        
        if success:
            print(f"  ✓ Completed T = {T} K")
            results[T] = "success"
        else:
            print(f"  ✗ Failed T = {T} K")
            print(f"  Error: {output[:200]}")
            results[T] = "failed"
    
    print("\n" + "=" * 60)
    print("Summary:")
    for T, status in results.items():
        print(f"  T = {T} K: {status}")
    
    return results

if __name__ == "__main__":
    main()

