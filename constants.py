"""
Physical constants and parameters for MD simulations and DSA analysis.
"""

import numpy as np

# Physical constants
k_B = 8.617e-5  # eV/K
R = 8.314  # J/(mol·K)
N_A = 6.022e23  # Avogadro's number

# Material properties
b = 2.86e-10  # Burgers vector (m)
epsilon_dot = 1e-3  # Strain rate (s^-1)
rho_m_values = [1e12, 1e13, 1e14]  # Mobile dislocation density (m^-2)

# Composition
Mg_weight_percent = 5.0  # wt%
# Convert to atomic percent: Al-5wt%Mg ≈ 5.52 at% Mg
# Using atomic weights: Al = 26.98, Mg = 24.31
# x_Mg = (5/24.31) / (5/24.31 + 95/26.98) ≈ 0.0552
Mg_atomic_percent = 5.52  # at%

# MD simulation parameters (Updated per professor advice)
timestep = 1e-15  # 1 fs in seconds
timestep_lammps = 0.001  # 1 fs in LAMMPS metal units (ps)

# Per professor advice: Can use shorter times at higher temperatures
# 1 ns = 100,000 steps is doable
# Higher T = faster atomic movement = easier MSD calculation
equilibration_time = 0.1  # ns (100,000 steps)
production_time = 1.0  # ns (100,000 steps) - shorter at higher T is acceptable
equilibration_steps = int(equilibration_time * 1000 / timestep_lammps)  # 100,000 steps
production_steps = int(production_time * 1000 / timestep_lammps)  # 100,000 steps

# Temperature ranges (Updated per professor feedback)
# Use 3 temperatures below melting point (~933 K for Al)
T_md = [500, 600, 700]  # K (for MD simulations - 3 temperatures as specified)
T_dsa = np.linspace(300, 450, 16)  # K (for DSA analysis)

# Validation thresholds
lattice_tolerance = 0.01  # ±1% for lattice constant
cohesive_tolerance = 0.05  # ±5% for cohesive energy
msd_r2_threshold = 0.95  # R² > 0.95 for MSD linearity
temp_stability = 20.0  # ±20 K temperature stability
energy_drift_threshold = 0.01  # eV/atom/ns

# Experimental reference values (Al)
a0_exp = 4.049  # Å (lattice constant at 300 K)
E_cohesive_exp = -3.39  # eV/atom (cohesive energy)

# DSA length scales (Updated per professor feedback)
# CRITICAL: Two DIFFERENT L values must be used - this was the key correction!
#
# L_c (capture radius): nm scale, used in τ_diff = L_c² / D_eff
#   - Physical meaning: Distance over which solute (Mg) can be captured by dislocation
#   - Typical range: 1-10 nm (from literature or binding energy considerations)
#   - Used for: Diffusion time calculation
L_capture = np.array([1.0, 2.0, 5.0]) * 1e-9  # Capture radius (m) - nm scale

# L_t (travel distance): µm scale, used in τ_wait = L_t / (ρ_m * b * ε̇)
#   - Physical meaning: Average distance dislocation travels before being pinned
#   - Typical range: 0.1-10 µm (depends on microstructure and deformation)
#   - Used for: Waiting time calculation
#   - NOTE: This is NOT the same as L_c! They have different physical meanings!
L_travel = np.array([0.1, 1.0, 10.0]) * 1e-6  # Travel distance (m) - µm scale

# Pipe diffusion factor (analytical correction, no MD needed)
# D_eff = D_bulk * (1 + f_pipe)
# f_pipe = 0 means pure bulk diffusion
# f_pipe > 0 accounts for enhanced diffusion near dislocations
f_pipe = 1.0  # Default: 2× bulk D (D_eff = 2×D_bulk). Can vary 0.1-10 for sensitivity

# LAMMPS units
LAMMPS_UNITS = "metal"  # eV, Angstrom, ps, etc.


