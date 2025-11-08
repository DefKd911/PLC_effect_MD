# Interatomic Potentials

Place your EAM potential file for Al-Mg here.

## Required File

- `EAM_AlMg.eam.alloy` - EAM potential file for Al-Mg system

## Where to Find Al-Mg EAM Potentials

### 1. NIST Interatomic Potentials Repository (Recommended)

**Direct Link:** https://www.ctcms.nist.gov/potentials/system/Al-Mg/

**Steps:**
1. Visit the NIST repository link above
2. Browse available Al-Mg potentials (e.g., Liu et al., Mendelev et al.)
3. Download the potential file (usually in `.eam` or `.eam.alloy` format)
4. Rename it to `EAM_AlMg.eam.alloy` and place it in this directory

**Popular choices:**
- **Liu et al. potential** - Well-tested for Al-Mg systems
- **Mendelev et al. potential** - Commonly used in literature

### 2. OpenKIM Repository

**Direct Link:** https://openkim.org/

**Steps:**
1. Go to https://openkim.org/
2. Search for "Al-Mg EAM" or "Al Mg"
3. Look for potentials like:
   - `EAM_Dynamo_MendelevAstaRahman_2009_AlMg__MO_658278549784_005`
4. Download the potential file
5. Convert to LAMMPS format if needed (some may need conversion)

### 3. Literature Sources

Search for these papers and check supplementary materials:

- **Zhou et al. (2004)**: "Embedded-atom-method potential for Al-Mg system"
- **Mendelev et al. (2009)**: "Development of new interatomic potentials appropriate for crystalline and liquid Al-Mg"
- **Liu et al.**: Various Al-Mg EAM potentials

**How to find:**
- Google Scholar: Search "Al-Mg EAM potential LAMMPS"
- Check paper supplementary materials
- Contact authors for potential files

### 4. Quick Download Options

**Option A: NIST Repository (Easiest)**
```
1. Visit: https://www.ctcms.nist.gov/potentials/system/Al-Mg/
2. Click on a potential (e.g., "Liu et al.")
3. Download the .eam or .eam.alloy file
4. Rename to EAM_AlMg.eam.alloy
5. Place in this directory
```

**Option B: OpenKIM**
```
1. Visit: https://openkim.org/
2. Search: "Al Mg EAM"
3. Download potential file
4. Place in this directory (may need format conversion)
```

## Potential Format

The LAMMPS input scripts expect an **EAM/alloy** potential file format. Most repositories provide files in this format or compatible formats.

**File format check:**
- Should start with comment lines (beginning with #)
- Contains density and embedding function data
- Usually has `.eam`, `.eam.alloy`, or `.eam.fs` extension

## Format Conversion (if needed)

If you have a potential in a different format, you may need to convert it:

```bash
# LAMMPS provides conversion tools
# Check LAMMPS documentation for convert_eam utility
```

## Validation

After placing the potential file:

1. Check that the file exists: `ls potentials/EAM_AlMg.eam.alloy`
2. Run a test simulation to verify it works
3. Check LAMMPS log for any potential-related errors

## Recommended Potential for This Study

For Al-5wt%Mg diffusion studies, the **Mendelev et al. (2009)** or **Liu et al.** potentials from NIST are recommended as they:
- Are well-tested for Al-Mg systems
- Reproduce experimental properties reasonably
- Are compatible with LAMMPS EAM/alloy format

## Troubleshooting

**"Potential file not found"**
- Ensure file is named exactly: `EAM_AlMg.eam.alloy`
- Check file is in `potentials/` directory
- Verify file path in LAMMPS input scripts

**"Potential format error"**
- Ensure file is in EAM/alloy format
- Check LAMMPS documentation for format requirements
- Try a different potential from NIST repository

**"Simulation crashes"**
- Verify potential is appropriate for your temperature range
- Check potential is for Al-Mg (not just Al)
- Review potential documentation for limitations

