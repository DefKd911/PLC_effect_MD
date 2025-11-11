import sys
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats

if len(sys.argv) < 2:
    print("Usage: python analyze_interface_msd.py <msd_file>")
    sys.exit(1)

filename = Path(sys.argv[1])
if not filename.exists():
    print(f"File not found: {filename}")
    sys.exit(1)

cols = [
    'step','Mg_x','Mg_y','Mg_z','Mg_total',
    'Al_x','Al_y','Al_z','Al_total'
]

try:
    data = pd.read_csv(filename, delim_whitespace=True, comment='#', header=None, names=cols)
except Exception as exc:
    print(f"Error reading {filename}: {exc}")
    sys.exit(1)

ps_per_step = 0.001
step0 = data['step'].iloc[0]
time_ps = (data['step'] - step0) * ps_per_step
# convert to seconds
TIME = time_ps * 1e-12

results = []
for species, column in [('Mg','Mg_z'), ('Al','Al_z')]:
    msd_ang = data[column]
    msd_m2 = msd_ang * 1e-20
    # discard first 20% of data to minimize transients
    cut_index = int(len(msd_m2) * 0.2)
    t = TIME[cut_index:]
    m = msd_m2[cut_index:]
    if len(t) < 10:
        print(f"Not enough data points after cut for {species}")
        continue
    slope, intercept, r_value, p_value, std_err = stats.linregress(t, m)
    D = slope / 2.0
    results.append({
        'species': species,
        'D_m2_per_s': D,
        'slope': slope,
        'intercept': intercept,
        'R2': r_value ** 2,
        'std_err': std_err / 2.0,
        'points': len(t)
    })

if not results:
    print("No results computed.")
    sys.exit(0)

for res in results:
    print(f"Species: {res['species']}")
    print(f"  Points used: {res['points']}")
    print(f"  Diffusivity D: {res['D_m2_per_s']:.3e} m^2/s")
    print(f"  R^2: {res['R2']:.4f}")
    print(f"  Std err: {res['std_err']:.3e} m^2/s")
    print()
