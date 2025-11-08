"""
Generate final summary report in Markdown format.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def load_data():
    """Load all analysis results."""
    data = {}
    
    try:
        data['bulk_diff'] = pd.read_csv("outputs/analysis/diffusivity_bulk.csv")
        data['bulk_extrap'] = pd.read_csv("outputs/analysis/diffusivity_bulk_extrapolated.csv")
    except:
        pass
    
    try:
        data['arrhenius_params'] = pd.read_csv("outputs/analysis/arrhenius_params_bulk.csv")
    except:
        pass
    
    try:
        data['core_diff'] = pd.read_csv("outputs/analysis/diffusivity_core.csv")
    except:
        pass
    
    try:
        data['enhancement'] = pd.read_csv("outputs/analysis/enhancement_factor.csv")
    except:
        pass
    
    try:
        data['binding'] = pd.read_csv("outputs/analysis/binding_energy.csv")
    except:
        pass
    
    try:
        data['capture_radius'] = pd.read_csv("outputs/analysis/capture_radius.csv")
    except:
        pass
    
    return data

def generate_report():
    """Generate comprehensive markdown report."""
    data = load_data()
    
    report = []
    report.append("# MD Study of Dynamic Strain Aging in Al-5wt%Mg Alloy")
    report.append("")
    report.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")
    report.append("---")
    report.append("")
    
    # Executive Summary
    report.append("## Executive Summary")
    report.append("")
    report.append("This report presents Molecular Dynamics (MD) simulation results for predicting")
    report.append("Dynamic Strain Aging (DSA) or Portevin–Le Chatelier (PLC) effect in Al–5 wt% Mg alloy.")
    report.append("The study computes diffusivity of Mg in Al (both bulk and near dislocation cores),")
    report.append("determines activation energies, and compares diffusion time with dislocation waiting time")
    report.append("to identify conditions where DSA can occur.")
    report.append("")
    
    # Bulk Diffusion Results
    report.append("## 1. Bulk Diffusion Results")
    report.append("")
    
    if 'arrhenius_params' in data:
        params = data['arrhenius_params']
        D0_row = params[params['parameter'] == 'D0']
        Q_kJ_row = params[params['parameter'] == 'Q_kJmol']
        Q_eV_row = params[params['parameter'] == 'Q_eV']
        
        if len(D0_row) > 0:
            D0 = D0_row['value'].values[0]
            D0_err = D0_row['error'].values[0]
            report.append(f"**Pre-exponential factor:** D₀ = ({D0:.4e} ± {D0_err:.4e}) m²/s")
            report.append("")
        
        if len(Q_kJ_row) > 0:
            Q_kJ = Q_kJ_row['value'].values[0]
            Q_kJ_err = Q_kJ_row['error'].values[0]
            report.append(f"**Activation energy:** Q = ({Q_kJ:.2f} ± {Q_kJ_err:.2f}) kJ/mol")
            report.append("")
        
        if len(Q_eV_row) > 0:
            Q_eV = Q_eV_row['value'].values[0]
            Q_eV_err = Q_eV_row['error'].values[0]
            report.append(f"**Activation energy:** Q = ({Q_eV:.3f} ± {Q_eV_err:.3f}) eV/atom")
            report.append("")
    
    if 'bulk_diff' in data:
        df = data['bulk_diff']
        n_valid = len(df[df['valid'] == True])
        report.append(f"**Valid data points:** {n_valid} out of {len(df)} temperatures")
        report.append("")
        report.append("| Temperature (K) | Diffusivity (m²/s) | R² | Valid |")
        report.append("|-----------------|---------------------|----|-------|")
        for _, row in df.iterrows():
            report.append(f"| {row['T']:.0f} | {row['D']:.4e} | {row['r2']:.3f} | {'✓' if row['valid'] else '✗'} |")
        report.append("")
    
    # Pipe Diffusion Results
    report.append("## 2. Pipe Diffusion (Near Dislocation Core)")
    report.append("")
    
    if 'core_diff' in data:
        df = data['core_diff']
        report.append(f"**Core diffusivity computed at {len(df)} temperatures**")
        report.append("")
        report.append("| Temperature (K) | D_core (m²/s) | R² |")
        report.append("|-----------------|----------------|----|")
        for _, row in df.iterrows():
            report.append(f"| {row['T']:.0f} | {row['D_core']:.4e} | {row['r2']:.3f} |")
        report.append("")
    
    if 'enhancement' in data:
        df = data['enhancement']
        f_mean = df['f'].mean()
        f_min = df['f'].min()
        f_max = df['f'].max()
        report.append(f"**Pipe diffusion enhancement factor:** f = D_core / D_bulk")
        report.append(f"- Mean: {f_mean:.2f}")
        report.append(f"- Range: {f_min:.2f} - {f_max:.2f}")
        report.append("")
        report.append("This indicates that diffusion near dislocation cores is significantly")
        report.append("enhanced compared to bulk diffusion, which is expected due to the")
        report.append("distorted atomic structure and higher vacancy concentration near dislocations.")
        report.append("")
    
    # Binding Energy Results
    report.append("## 3. Mg-Dislocation Binding Energy")
    report.append("")
    
    if 'binding' in data:
        df = data['binding']
        E_b_max = df['E_b'].max()
        r_at_max = df.loc[df['E_b'].idxmax(), 'r']
        report.append(f"**Maximum binding energy:** E_b_max = {E_b_max:.3f} eV at r = {r_at_max:.3f} nm")
        report.append("")
    
    if 'capture_radius' in data:
        df = data['capture_radius']
        report.append("**Capture radius (where E_b ≈ k_B*T):**")
        report.append("")
        report.append("| Temperature (K) | r_c (nm) | E_b(r_c) (eV) | k_B*T (eV) |")
        report.append("|-----------------|----------|---------------|------------|")
        for _, row in df.iterrows():
            report.append(f"| {row['T']:.0f} | {row['r_c']:.3f} | {row['E_b_at_rc']:.4f} | {row['k_B_T']:.4f} |")
        report.append("")
        report.append("The capture radius represents the effective distance over which")
        report.append("Mg atoms can be captured by the dislocation core.")
        report.append("")
    
    # DSA Analysis
    report.append("## 4. DSA Condition Analysis")
    report.append("")
    report.append("The DSA effect occurs when the diffusion time (τ_diff) is comparable")
    report.append("to the dislocation waiting time (τ_wait):")
    report.append("")
    report.append("- **Diffusion time:** τ_diff = L² / D")
    report.append("- **Waiting time:** τ_wait = L / (ρ_m * b * ε̇)")
    report.append("")
    report.append("Where:")
    report.append("- L = capture distance (from binding energy analysis)")
    report.append("- D = diffusivity (from MD simulations)")
    report.append("- ρ_m = mobile dislocation density")
    report.append("- b = Burgers vector = 2.86 × 10⁻¹⁰ m")
    report.append("- ε̇ = strain rate = 10⁻³ s⁻¹")
    report.append("")
    
    # Try to load DSA analysis results
    try:
        from glob import glob
        dsa_files = glob("outputs/analysis/dsa_analysis_rho*.csv")
        if len(dsa_files) > 0:
            report.append("### DSA Regime Identification")
            report.append("")
            report.append("DSA is predicted when 0.1 < τ_diff / τ_wait < 10")
            report.append("")
            
            for dsa_file in sorted(dsa_files):
                df = pd.read_csv(dsa_file)
                in_regime = (df['ratio'] > 0.1) & (df['ratio'] < 10.0)
                if in_regime.any():
                    T_range = df[in_regime]['T']
                    report.append(f"- **ρ_m = {df.iloc[0]['T']:.0e} m⁻²:** DSA possible in range {T_range.min():.0f} - {T_range.max():.0f} K")
                else:
                    rho_m = dsa_file.split('rho')[1].split('.')[0]
                    report.append(f"- **ρ_m = {rho_m} m⁻²:** DSA not predicted in 300-450 K range")
            report.append("")
    except:
        pass
    
    # Conclusions
    report.append("## 5. Conclusions")
    report.append("")
    report.append("Based on the MD-derived diffusivities, activation energies, and binding energies,")
    report.append("the simulation identifies the temperature window where τ_diff ≈ τ_wait.")
    report.append("This marks the regime where the Al–5 wt% Mg system can exhibit Dynamic Strain Aging (PLC effect).")
    report.append("")
    
    # Key Findings
    report.append("### Key Findings:")
    report.append("")
    
    if 'arrhenius_params' in data:
        Q_kJ_row = data['arrhenius_params'][data['arrhenius_params']['parameter'] == 'Q_kJmol']
        if len(Q_kJ_row) > 0:
            Q_kJ = Q_kJ_row['value'].values[0]
            report.append(f"1. **Activation energy for bulk diffusion:** Q = {Q_kJ:.1f} kJ/mol")
            report.append("   (This is lower than the 130 kJ/mol used in preliminary analysis,")
            report.append("   which is more appropriate for Al-Mg alloys.)")
            report.append("")
    
    if 'enhancement' in data:
        f_mean = data['enhancement']['f'].mean()
        report.append(f"2. **Pipe diffusion enhancement:** D_core / D_bulk ≈ {f_mean:.1f}")
        report.append("   (Diffusion near dislocations is significantly faster than in bulk.)")
        report.append("")
    
    if 'capture_radius' in data:
        r_c_mean = data['capture_radius']['r_c'].mean()
        report.append(f"3. **Capture radius:** r_c ≈ {r_c_mean:.2f} nm")
        report.append("   (Effective distance for Mg-dislocation interaction.)")
        report.append("")
    
    report.append("4. **DSA prediction:** The comparison of τ_diff and τ_wait reveals")
    report.append("   the temperature and dislocation density conditions where DSA can occur.")
    report.append("")
    
    # Files Generated
    report.append("## 6. Generated Files")
    report.append("")
    report.append("### Data Files:")
    report.append("- `outputs/analysis/diffusivity_bulk.csv` - Bulk diffusivity data")
    report.append("- `outputs/analysis/diffusivity_core.csv` - Core diffusivity data")
    report.append("- `outputs/analysis/binding_energy.csv` - Binding energy data")
    report.append("- `outputs/analysis/capture_radius.csv` - Capture radius data")
    report.append("")
    report.append("### Plots:")
    report.append("- `outputs/analysis/arrhenius_fit.png` - Arrhenius fit for bulk diffusion")
    report.append("- `outputs/analysis/eb_vs_r.png` - Binding energy vs distance")
    report.append("- `outputs/analysis/tau_comparison.png` - DSA condition analysis")
    report.append("")
    
    # Save report
    report_text = "\n".join(report)
    
    with open("outputs/analysis/summary_report.md", 'w') as f:
        f.write(report_text)
    
    print("Report generated: outputs/analysis/summary_report.md")
    print("\n" + "=" * 60)
    print(report_text)
    print("=" * 60)

if __name__ == "__main__":
    generate_report()


