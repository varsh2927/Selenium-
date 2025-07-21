# Selenium Environment Setup Guide

This guide will help you set up a proper virtual environment for running Selenium-based web automation scripts on Windows.

## Prerequisites

Before starting, ensure you have:
- Python 3.8+ installed on your system
- Git (optional, for version control)
- A modern web browser (Chrome recommended)

## Step 1: Check Python Installation

First, verify Python is installed and accessible:

```powershell
python --version
# or
python3 --version
```

If Python is not found, download and install it from [python.org](https://www.python.org/downloads/).

## Step 2: Create Virtual Environment

Navigate to your project directory and create a virtual environment:

```powershell
# Navigate to your project folder
cd C:\Selenium\Selenium

# Create virtual environment
python -m venv .venv
```

## Step 3: Activate Virtual Environment

Activate the virtual environment:

```powershell
# For Windows PowerShell
.venv\Scripts\Activate.ps1

# For Windows Command Prompt
.venv\Scripts\activate.bat

# For Git Bash
source .venv/Scripts/activate
```

You should see `(.venv)` at the beginning of your command prompt when activated.

## Step 4: Upgrade pip

Upgrade pip to the latest version:

```powershell
python -m pip install --upgrade pip
```

## Step 5: Install Dependencies

Install all required packages from requirements.txt:

```powershell
pip install -r requirements.txt
```

### If you encounter issues with lxml:

The `lxml` package sometimes fails to install on Windows. If this happens, try:

```powershell
# Method 1: Install pre-compiled wheel
pip install lxml --only-binary=all

# Method 2: Install Microsoft Visual C++ Build Tools first
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# Then try installing lxml again

# Method 3: Use conda instead (if you have Anaconda/Miniconda)
conda install lxml
```

## Step 6: Verify Installation

Run the diagnostic script to verify everything is working:

```powershell
python diagnose_errors.py
```

This will check:
- Python version
- Installed packages
- Chrome/ChromeDriver availability
- Web connectivity

## Step 7: Install ChromeDriver (if needed)

The scripts use `webdriver-manager` which should automatically download ChromeDriver. If you encounter issues:

```powershell
# Manual ChromeDriver installation
pip install webdriver-manager --upgrade
```

## Step 8: Test the Setup

Run a simple test to verify everything works:

```powershell
python working_test.py
```

This should open a browser window and perform a basic web automation test.

## Alternative Setup Methods

### Using Conda (Recommended for Windows)

If you have Anaconda or Miniconda installed:

```powershell
# Create conda environment
conda create -n selenium-env python=3.9

# Activate environment
conda activate selenium-env

# Install packages
conda install -c conda-forge selenium beautifulsoup4 requests pandas
pip install webdriver-manager fake-useragent pytest pytest-html openpyxl
```

### Using pipenv

```powershell
# Install pipenv
pip install pipenv

# Install dependencies
pipenv install -r requirements.txt

# Activate environment
pipenv shell
```

## Troubleshooting Common Issues

### 1. PowerShell Execution Policy Error

If you get an execution policy error when activating the virtual environment:

```powershell
# Run as Administrator and execute:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. ChromeDriver Issues

If ChromeDriver fails to download or run:

```powershell
# Clear webdriver-manager cache
pip uninstall webdriver-manager
pip install webdriver-manager --force-reinstall
```

### 3. Permission Errors

If you get permission errors during installation:

```powershell
# Run PowerShell as Administrator
# Or use user installation
pip install --user -r requirements.txt
```

### 4. Network Issues

If you're behind a corporate firewall:

```powershell
# Use proxy settings
pip install --proxy http://proxy.company.com:8080 -r requirements.txt
```

## Environment Variables (Optional)

You can set these environment variables for better control:

```powershell
# Set Chrome to run in headless mode (no browser window)
$env:CHROME_HEADLESS = "true"

# Set custom ChromeDriver path
$env:CHROMEDRIVER_PATH = "C:\path\to\chromedriver.exe"

# Set download directory for scraped data
$env:DOWNLOAD_DIR = "C:\Selenium\Selenium\downloads"
```

## Running Scripts

Once setup is complete, you can run scripts using:

```powershell
# Use the launcher (recommended)
python run_scripts.py

# Or run individual scripts
python web_automation.py
python web_scraping.py
python bot_creation.py
python web_testing.py
```

## Deactivating the Environment

When you're done working:

```powershell
deactivate
```

## Updating Dependencies

To update packages to their latest versions:

```powershell
# Activate environment first
.venv\Scripts\Activate.ps1

# Update all packages
pip install --upgrade -r requirements.txt
```

## Complete Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] pip upgraded
- [ ] All dependencies installed
- [ ] ChromeDriver working
- [ ] Diagnostic script passes
- [ ] Test script runs successfully

## Next Steps

After completing the setup:

1. Read `readme.md` for project overview
2. Check `TROUBLESHOOTING.md` for common issues
3. Review `link_ref.txt` for URLs used in scripts
4. Run `python run_scripts.py` to start using the launcher

## Support

If you encounter issues not covered in this guide:
1. Check `TROUBLESHOOTING.md`
2. Run `python diagnose_errors.py` for detailed diagnostics
3. Run `python fix_errors.py` for automatic fixes 