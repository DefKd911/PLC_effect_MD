"""
Main workflow script to run all simulations and analyses.
"""

import os
import sys
import subprocess

def run_script(script_name, description):
    """Run a Python script and report results."""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            return True
        else:
            print(f"✗ {description} failed")
            return False
    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False

def main():
    """Main workflow - Updated per professor feedback."""
    print("="*60)
    print("MD Study of DSA in Al-5wt%Mg Alloy")
    print("Updated Workflow (3 temperatures, optimized system)")
    print("="*60)
    
    # Step 1: Create system
    print("\nStep 1: Creating optimized bulk system...")
    run_script("scripts/create_bulk_system.py", "Creating bulk system (864 atoms)")
    
    # Step 2: Validate length scales
    print("\nStep 2: Validating length scales (L_c and L_t)...")
    run_script("scripts/compute_length_scales.py", "Length scale validation")
    
    # Step 3: Run simulations (if LAMMPS is available)
    print("\nStep 3: Running MD simulations...")
    print("Note: This requires LAMMPS to be installed and in PATH")
    print("      You need to run simulations at 3 temperatures: 500, 600, 700 K")
    print("      Each takes ~1-2 hours")
    
    run_sims = input("\nRun LAMMPS simulations now? (y/n): ").lower().strip() == 'y'
    
    if run_sims:
        print("\nRunning simulations at 3 temperatures...")
        print("This will take ~3-6 hours total.")
        print("You can also run them manually:")
        print("  lmp -in inputs/bulk/in.bulk_diffusion -var T 500 -log outputs/bulk/log_T500.log")
        print("  lmp -in inputs/bulk/in.bulk_diffusion -var T 600 -log outputs/bulk/log_T600.log")
        print("  lmp -in inputs/bulk/in.bulk_diffusion -var T 700 -log outputs/bulk/log_T700.log")
        
        # Run via script
        run_script("scripts/run_bulk_diffusion.py", "Running bulk diffusion simulations")
    
    # Step 4: Analyze results
    print("\nStep 4: Analyzing results...")
    
    # Check if data files exist
    msd_files = ["outputs/bulk/msd_T500.dat", "outputs/bulk/msd_T600.dat", "outputs/bulk/msd_T700.dat"]
    has_data = any(os.path.exists(f) for f in msd_files) or os.path.exists("outputs/analysis/diffusivity_bulk.csv")
    
    if has_data:
        run_script("scripts/analyze_msd.py", "Analyzing MSD data")
        run_script("scripts/fit_arrhenius.py", "Fitting Arrhenius equation")
    else:
        print("Warning: MSD data files not found.")
        print("Please run simulations first at 500, 600, 700 K")
        print("Then run: python scripts/analyze_msd.py")
    
    # Step 5: DSA analysis
    print("\nStep 5: DSA condition analysis...")
    required_file = "outputs/analysis/diffusivity_bulk_extrapolated.csv"
    
    if os.path.exists(required_file):
        run_script("scripts/analyze_dsa.py", "Analyzing DSA conditions")
    else:
        print("Warning: Extrapolated diffusivity data not found.")
        print("Please run fit_arrhenius.py first.")
    
    # Step 6: Generate plots and report
    print("\nStep 6: Generating plots and report...")
    run_script("scripts/plot_results.py", "Generating plots")
    run_script("scripts/generate_report.py", "Generating summary report")
    
    print("\n" + "="*60)
    print("Workflow completed!")
    print("="*60)
    print("\nCheck outputs/analysis/ for all results and plots.")
    print("See outputs/analysis/summary_report.md for the final report.")
    print("\nKey files:")
    print("  - outputs/analysis/diffusivity_bulk.csv")
    print("  - outputs/analysis/arrhenius_params_bulk.csv")
    print("  - outputs/analysis/tau_comparison.png")
    print("  - outputs/analysis/summary_report.md")

if __name__ == "__main__":
    main()


