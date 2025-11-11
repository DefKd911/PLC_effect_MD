"""
Plot MSD trends for all three temperatures together for comparison.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read all MSD data
temperatures = [500, 600, 700]
colors = ['blue', 'red', 'green']
timestep = 0.001  # ps

plt.figure(figsize=(12, 8))

for T, color in zip(temperatures, colors):
    try:
        data = pd.read_csv(f'outputs/bulk/msd_T{T}.dat', sep=r'\s+', skiprows=3, 
                          names=['step', 'msd_x', 'msd_y', 'msd_z', 'msd_total'],
                          comment='#')
        
        time = data['step'].values * timestep  # ps
        msd = data['msd_total'].values  # Angstrom²
        
        plt.plot(time, msd, color=color, linewidth=2, label=f'T = {T} K', alpha=0.7)
        
        # Print statistics
        print(f"T = {T} K: Mean = {msd.mean():.4f} Å², Std = {msd.std():.4f} Å²")
    except Exception as e:
        print(f"Error reading T = {T} K: {e}")

plt.xlabel('Time (ps)', fontsize=14)
plt.ylabel('MSD (Å²)', fontsize=14)
plt.title('MSD vs Time: Comparison of All Temperatures', fontsize=16, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)
plt.tight_layout()
plt.savefig('outputs/analysis/msd_trend_all_temperatures.png', dpi=150, bbox_inches='tight')
print(f"\nComparison plot saved to outputs/analysis/msd_trend_all_temperatures.png")


