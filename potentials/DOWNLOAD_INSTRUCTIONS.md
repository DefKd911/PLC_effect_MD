# How to Download Al-Mg EAM Potential

## Quick Guide

### Method 1: NIST Repository (Recommended - Easiest)

1. **Visit NIST Potentials Repository:**
   - Go to: https://www.ctcms.nist.gov/potentials/system/Al-Mg/
   - Or search: "NIST interatomic potentials Al-Mg"

2. **Select a Potential:**
   - Recommended: **Liu et al.** or **Mendelev et al.**
   - Click on the potential name to view details

3. **Download:**
   - Look for download link (usually "Download potential" or similar)
   - File will be named something like `AlMg.eam.alloy` or `AlMg.eam`

4. **Rename and Place:**
   ```bash
   # Rename the downloaded file
   mv downloaded_file.eam.alloy potentials/EAM_AlMg.eam.alloy
   ```

### Method 2: OpenKIM

1. **Visit OpenKIM:**
   - Go to: https://openkim.org/
   - Click "Models" → Search for "Al Mg EAM"

2. **Find Suitable Potential:**
   - Look for: `EAM_Dynamo_MendelevAstaRahman_2009_AlMg`
   - Or search: "Al Mg embedded atom method"

3. **Download:**
   - Click on the model
   - Download the potential file
   - May need to extract from archive

4. **Place in Directory:**
   ```bash
   cp downloaded_file potentials/EAM_AlMg.eam.alloy
   ```

### Method 3: From Research Papers

1. **Search Literature:**
   - Google Scholar: "Al-Mg EAM potential LAMMPS"
   - Look for papers by: Zhou, Mendelev, Liu, etc.

2. **Check Supplementary Materials:**
   - Many papers provide potential files as supplementary data
   - Check journal website or author's personal page

3. **Contact Authors:**
   - Email corresponding author
   - Request the potential file used in their study

## Specific Recommendations

### For Diffusion Studies (This Project)

**Best Choice:** Mendelev et al. (2009) or Liu et al. potential
- Well-tested for Al-Mg diffusion
- Reproduces experimental diffusion coefficients
- Available on NIST repository

**NIST Direct Links:**
- Al-Mg system page: https://www.ctcms.nist.gov/potentials/system/Al-Mg/
- Search for "Mendelev" or "Liu" in the list

### File Naming

After downloading, ensure the file is named:
```
potentials/EAM_AlMg.eam.alloy
```

The scripts expect this exact name and location.

## Verification

After downloading, verify the file:

```bash
# Check file exists
ls -lh potentials/EAM_AlMg.eam.alloy

# Check file is not empty
wc -l potentials/EAM_AlMg.eam.alloy

# View first few lines (should start with comments)
head -20 potentials/EAM_AlMg.eam.alloy
```

## Example: Downloading from NIST

1. Visit: https://www.ctcms.nist.gov/potentials/system/Al-Mg/
2. You'll see a table with available potentials
3. Click on one (e.g., "Liu et al.")
4. On the potential page, find the download section
5. Download the `.eam.alloy` file
6. Save as `potentials/EAM_AlMg.eam.alloy`

## Troubleshooting Downloads

**"Link not working"**
- Try accessing NIST repository directly
- Check if site is temporarily down
- Try OpenKIM as alternative

**"File format unclear"**
- EAM files usually have `.eam`, `.eam.alloy`, or `.eam.fs` extension
- Check file header - should contain "#" comment lines
- LAMMPS can read most EAM formats

**"Multiple files downloaded"**
- Usually you need the `.eam.alloy` file
- Other files may be documentation or different formats
- Use the `.eam.alloy` file for LAMMPS

## Need Help?

If you can't find a suitable potential:
1. Check NIST repository first (most reliable)
2. Try OpenKIM as backup
3. Search recent literature for new potentials
4. Consider contacting potential developers

Most Al-Mg EAM potentials should work, but some may be optimized for specific properties (e.g., mechanical vs. diffusion). For diffusion studies, Mendelev or Liu potentials are typically good choices.


