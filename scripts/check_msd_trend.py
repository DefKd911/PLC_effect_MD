"""
Quick script to visualize MSD trend at 500 K.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read MSD data
data = pd.read_csv('outputs/bulk/msd_T500.dat', sep=r'\s+', skiprows=3, 
                  names=['step', 'msd_x', 'msd_y', 'msd_z', 'msd_total'],
                  comment='#')

# Convert step to time (ps)
timestep = 0.001  # ps
time = data['step'].values * timestep  # ps
msd = data['msd_total'].values  # Angstrom²

# Plot
plt.figure(figsize=(10, 6))
plt.plot(time, msd, 'b-', linewidth=2, label='MSD (Total)')
plt.xlabel('Time (ps)', fontsize=12)
plt.ylabel('MSD (Å²)', fontsize=12)
plt.title('MSD vs Time at 500 K', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig('outputs/analysis/msd_trend_T500.png', dpi=150)
print(f"MSD range: {msd.min():.4f} to {msd.max():.4f} Å²")
print(f"MSD mean: {msd.mean():.4f} Å²")
print(f"MSD std: {msd.std():.4f} Å²")
print(f"Time range: {time.min():.1f} to {time.max():.1f} ps")
print(f"\nPlot saved to outputs/analysis/msd_trend_T500.png")


