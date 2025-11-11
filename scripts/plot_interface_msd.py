import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

msd_file = Path('outputs/interface_1k/msd_interface_T700.dat')
cols = ['step','Mg_x','Mg_y','Mg_z','Mg_total','Al_x','Al_y','Al_z','Al_total']
data = pd.read_csv(msd_file, sep=r'\s+', comment='#', header=None, names=cols)

step0 = data['step'].iloc[0]
time_ps = (data['step'] - step0) * 0.001
time_ns = time_ps / 1000.0

start_ns = 0.1 if time_ns.max() >= 0.1 else 0.2 * time_ns.max()
mask = time_ns >= start_ns

def fit_line(x, y):
    coeffs = np.polyfit(x, y, 1)
    return coeffs, np.poly1d(coeffs)

plt.figure(figsize=(8,6))

for species, column, color in [
    ('Mg', 'Mg_z', 'tab:blue'),
    ('Al', 'Al_z', 'tab:orange'),
]:
    y = data[column]
    plt.plot(time_ns, y, label=f'{species} MSD (z)', color=color, alpha=0.7)

    if np.count_nonzero(mask) > 1:
        coeffs, fit_fn = fit_line(time_ns[mask], y[mask])
        plt.plot(
            time_ns[mask],
            fit_fn(time_ns[mask]),
            linestyle='--',
            color=color,
            label=f'{species} fit: slope={coeffs[0]:.2f} Å²/ns'
        )

plt.xlabel('Time (ns)')
plt.ylabel('MSD (Å²)')
plt.title('Interface-normal MSD vs Time at 850 K (1k atoms)')
plt.xlim(0.0, time_ns.max())
plt.grid(alpha=0.3)
plt.legend()

Path('outputs/analysis').mkdir(parents=True, exist_ok=True)
plt.tight_layout()
plt.savefig('outputs/analysis/msd_trend_interface_T700_1k.png', dpi=150)
