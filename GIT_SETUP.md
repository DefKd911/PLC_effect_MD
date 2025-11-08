# Git/GitHub Setup Guide

## Issue: "src refspec main does not match any"

This error means:
- No local branch named "main" exists, OR
- No commits have been made yet

## Solution: Initialize and Push to GitHub

### Step 1: Check Git Status
```bash
git status
```

### Step 2: Initialize Repository (if needed)
```bash
# Only if .git doesn't exist
git init
```

### Step 3: Add All Files
```bash
git add .
```

### Step 4: Make Initial Commit
```bash
git commit -m "Initial commit: MD study of DSA in Al-5wt%Mg"
```

### Step 5: Create Main Branch (if needed)
```bash
# If branch is "master", rename it
git branch -M main
```

### Step 6: Add Remote (if not already added)
```bash
git remote add origin https://github.com/DefKd911/PLC_effect_MD.git
# Or if already exists:
git remote set-url origin https://github.com/DefKd911/PLC_effect_MD.git
```

### Step 7: Push to GitHub
```bash
git push -u origin main
```

## Complete Command Sequence

```bash
# Initialize (if needed)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: MD study of DSA in Al-5wt%Mg"

# Ensure main branch
git branch -M main

# Add remote
git remote add origin https://github.com/DefKd911/PLC_effect_MD.git
# Or update if exists:
# git remote set-url origin https://github.com/DefKd911/PLC_effect_MD.git

# Push
git push -u origin main
```

## What to Exclude (Gitignore)

Make sure `.gitignore` includes:
- Large output files (trajectories, logs)
- Python cache (`__pycache__/`)
- Large data files

The `.gitignore` file should already be set up.

