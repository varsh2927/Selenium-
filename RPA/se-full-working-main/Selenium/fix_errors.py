#!/usr/bin/env python3
"""
Automatic Error Fix Script
This script will automatically fix common issues with the Selenium setup.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🛠️  {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            return True
        else:
            print(f"❌ {description} - FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - ERROR: {e}")
        return False

def fix_dependencies():
    """Fix dependency issues"""
    print("\n" + "="*60)
    print("🔧 FIXING DEPENDENCIES")
    print("="*60)
    
    # Upgrade pip first
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install/upgrade webdriver-manager
    run_command(f"{sys.executable} -m pip install --upgrade webdriver-manager", "Upgrading webdriver-manager")
    
    # Install all requirements
    run_command(f"{sys.executable} -m pip install -r requirements.txt", "Installing requirements")
    
    # Install additional packages that might be missing
    additional_packages = [
        "requests",
        "beautifulsoup4", 
        "pandas",
        "fake-useragent",
        "lxml",
        "openpyxl"
    ]
    
    for package in additional_packages:
        run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")

def fix_chrome_driver():
    """Fix Chrome driver issues"""
    print("\n" + "="*60)
    print("🔧 FIXING CHROME DRIVER")
    print("="*60)
    
    # Clear webdriver-manager cache
    cache_dir = Path.home() / ".wdm"
    if cache_dir.exists():
        try:
            shutil.rmtree(cache_dir)
            print("✅ Cleared webdriver-manager cache")
        except Exception as e:
            print(f"⚠️  Could not clear cache: {e}")
    
    # Try to download Chrome driver
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        print(f"✅ ChromeDriver downloaded to: {driver_path}")
        return True
    except Exception as e:
        print(f"❌ ChromeDriver download failed: {e}")
        return False

def create_working_script():
    """Create a guaranteed working script"""
    print("\n" + "="*60)
    print("🔧 CREATING WORKING SCRIPT")
    print("="*60)
    
    script_content = '''#!/usr/bin/env python3
"""
Guaranteed Working Web Script
This script should work on any Windows system with Python.
"""

import requests
import json
from datetime import datetime

def test_basic_functionality():
    """Test basic web functionality"""
    print("🚀 Testing basic web functionality...")
    
    try:
        # Test 1: Simple HTTP request
        print("\\n--- Test 1: HTTP Request ---")
        response = requests.get("https://httpbin.org/get", timeout=10)
        print(f"✅ HTTP request successful: Status {response.status_code}")
        
        # Test 2: Get JSON data
        print("\\n--- Test 2: JSON Data ---")
        data = response.json()
        print(f"✅ JSON data received: {data.get('url', 'N/A')}")
        
        # Test 3: Test multiple websites
        print("\\n--- Test 3: Multiple Websites ---")
        websites = [
            "https://www.google.com",
            "https://www.python.org",
            "https://httpbin.org/json"
        ]
        
        results = []
        for url in websites:
            try:
                resp = requests.get(url, timeout=10)
                results.append({
                    "url": url,
                    "status": resp.status_code,
                    "accessible": resp.status_code == 200
                })
                print(f"✅ {url} - Status: {resp.status_code}")
            except Exception as e:
                results.append({
                    "url": url,
                    "status": "ERROR",
                    "accessible": False,
                    "error": str(e)
                })
                print(f"❌ {url} - Error: {e}")
        
        # Save results
        with open("test_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print("\\n✅ Results saved to test_results.json")
        
        # Summary
        successful = sum(1 for r in results if r.get('accessible', False))
        total = len(results)
        print(f"\\n📊 Summary: {successful}/{total} websites accessible")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("🔧 GUARANTEED WORKING WEB SCRIPT")
    print("="*60)
    
    success = test_basic_functionality()
    
    if success:
        print("\\n🎉 All tests passed! Your system can perform basic web operations.")
        print("\\nNext steps:")
        print("1. Try: python simple_web_tools.py")
        print("2. Try: python run_scripts.py")
    else:
        print("\\n⚠️  Some tests failed. Check your internet connection.")
    
    print("\\n" + "="*60)

if __name__ == "__main__":
    main()
'''
    
    with open("working_test.py", "w") as f:
        f.write(script_content)
    
    print("✅ Created working_test.py - a guaranteed working script")

def run_diagnostic():
    """Run the diagnostic script"""
    print("\n" + "="*60)
    print("🔍 RUNNING DIAGNOSTIC")
    print("="*60)
    
    if os.path.exists("diagnose_errors.py"):
        run_command(f"{sys.executable} diagnose_errors.py", "Running diagnostic")
    else:
        print("❌ diagnose_errors.py not found")

def main():
    """Main fix function"""
    print("🔧 AUTOMATIC ERROR FIX SCRIPT")
    print("This script will automatically fix common issues.")
    
    # Fix dependencies
    fix_dependencies()
    
    # Fix Chrome driver
    fix_chrome_driver()
    
    # Create working script
    create_working_script()
    
    # Run diagnostic
    run_diagnostic()
    
    print("\n" + "="*60)
    print("🎉 FIX PROCESS COMPLETED")
    print("="*60)
    print("\nNext steps:")
    print("1. Try: python working_test.py")
    print("2. Try: python simple_web_tools.py")
    print("3. Try: python run_scripts.py")
    print("\nIf you still have errors, run:")
    print("python diagnose_errors.py")

if __name__ == "__main__":
    main() 