#!/usr/bin/env python3
"""
Comprehensive Error Diagnostic Script
This script will identify all possible issues and provide specific solutions.
"""

import sys
import os
import subprocess
import platform
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_section(title):
    """Print a section header"""
    print(f"\n--- {title} ---")

def check_python_version():
    """Check Python version and compatibility"""
    print_section("Python Version Check")
    
    version = sys.version_info
    print(f"Python Version: {version.major}.{version.minor}.{version.micro}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7+ is required!")
        return False
    else:
        print("✅ Python version is compatible")
        return True

def check_python_path():
    """Check Python installation and PATH"""
    print_section("Python Installation Check")
    
    print(f"Python Executable: {sys.executable}")
    print(f"Python Path: {sys.path[0]}")
    
    # Check if pip is available
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip is available: {result.stdout.strip()}")
        else:
            print("❌ pip is not working properly")
            return False
    except Exception as e:
        print(f"❌ Error checking pip: {e}")
        return False
    
    return True

def check_dependencies():
    """Check all required dependencies"""
    print_section("Dependency Check")
    
    dependencies = {
        "selenium": "selenium",
        "webdriver_manager": "webdriver_manager",
        "requests": "requests",
        "beautifulsoup4": "bs4",
        "pandas": "pandas",
        "fake_useragent": "fake_useragent",
        "lxml": "lxml",
        "openpyxl": "openpyxl"
    }
    
    missing = []
    installed = []
    
    for package, import_name in dependencies.items():
        try:
            __import__(import_name)
            installed.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - MISSING")
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nTo install missing packages:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Or install individually:")
        for package in missing:
            print(f"   pip install {package}")
        return False
    else:
        print(f"\n✅ All {len(installed)} dependencies are installed!")
        return True

def check_chrome_installation():
    """Check Chrome browser installation"""
    print_section("Chrome Browser Check")
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expanduser(r"~\AppData\Local\Google\Chrome\Application\chrome.exe")
    ]
    
    chrome_found = False
    for path in chrome_paths:
        if os.path.exists(path):
            print(f"✅ Chrome found at: {path}")
            chrome_found = True
            break
    
    if not chrome_found:
        print("❌ Chrome browser not found!")
        print("Please install Google Chrome from: https://www.google.com/chrome/")
        return False
    
    return True

def test_webdriver_manager():
    """Test webdriver-manager functionality"""
    print_section("WebDriver Manager Test")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ webdriver-manager imported successfully")
        
        # Try to get Chrome driver path
        try:
            driver_path = ChromeDriverManager().install()
            print(f"✅ ChromeDriver path: {driver_path}")
            
            # Check if the file exists
            if os.path.exists(driver_path):
                print("✅ ChromeDriver file exists")
                return True
            else:
                print("❌ ChromeDriver file does not exist")
                return False
                
        except Exception as e:
            print(f"❌ Error getting ChromeDriver: {e}")
            return False
            
    except ImportError:
        print("❌ webdriver-manager not installed")
        return False

def test_selenium_basic():
    """Test basic Selenium functionality"""
    print_section("Basic Selenium Test")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        print("✅ Selenium imported successfully")
        
        # Test creating Chrome options
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        print("✅ Chrome options created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

def test_network_connectivity():
    """Test network connectivity"""
    print_section("Network Connectivity Test")
    
    try:
        import requests
        
        test_urls = [
            "https://www.google.com",
            "https://httpbin.org/get",
            "https://www.python.org"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                print(f"✅ {url} - Status: {response.status_code}")
            except Exception as e:
                print(f"❌ {url} - Error: {e}")
                return False
        
        return True
        
    except ImportError:
        print("❌ requests module not available")
        return False

def test_simple_web_tools():
    """Test the simple web tools script"""
    print_section("Simple Web Tools Test")
    
    try:
        # Import the simple web tools
        from simple_web_tools import SimpleWebTools
        
        print("✅ SimpleWebTools imported successfully")
        
        # Create instance
        tools = SimpleWebTools()
        print("✅ SimpleWebTools instance created")
        
        # Test basic functionality
        result = tools.test_website_connectivity("https://httpbin.org/get")
        if result and result.get('accessible'):
            print("✅ Basic web functionality works")
            return True
        else:
            print("❌ Basic web functionality failed")
            return False
            
    except Exception as e:
        print(f"❌ Simple web tools test failed: {e}")
        return False

def generate_report(results):
    """Generate a diagnostic report"""
    print_header("DIAGNOSTIC REPORT")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Generated: {timestamp}")
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"\n📊 Summary:")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_tests*100):.1f}%")
    
    print(f"\n📋 Detailed Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    # Provide recommendations
    print(f"\n💡 Recommendations:")
    
    if not results.get('python_version', False):
        print("- Update Python to version 3.7 or higher")
    
    if not results.get('dependencies', False):
        print("- Install missing dependencies: pip install -r requirements.txt")
    
    if not results.get('chrome_installation', False):
        print("- Install Google Chrome browser")
    
    if not results.get('webdriver_manager', False):
        print("- Reinstall webdriver-manager: pip install --upgrade webdriver-manager")
    
    if not results.get('network_connectivity', False):
        print("- Check your internet connection and firewall settings")
    
    if not results.get('simple_web_tools', False):
        print("- There are issues with the basic web tools - check the error messages above")
    
    # Final recommendation
    if results.get('simple_web_tools', False):
        print(f"\n🎉 Good news! You can use the simple web tools:")
        print("python simple_web_tools.py")
    else:
        print(f"\n⚠️  Fix the issues above before running the scripts")

def main():
    """Main diagnostic function"""
    print_header("COMPREHENSIVE ERROR DIAGNOSTIC")
    print("This script will identify all issues and provide solutions.")
    
    results = {}
    
    # Run all diagnostic tests
    results['python_version'] = check_python_version()
    results['python_path'] = check_python_path()
    results['dependencies'] = check_dependencies()
    results['chrome_installation'] = check_chrome_installation()
    results['webdriver_manager'] = test_webdriver_manager()
    results['selenium_basic'] = test_selenium_basic()
    results['network_connectivity'] = test_network_connectivity()
    results['simple_web_tools'] = test_simple_web_tools()
    
    # Generate report
    generate_report(results)
    
    print_header("NEXT STEPS")
    print("1. Fix any issues identified above")
    print("2. Try running: python simple_web_tools.py")
    print("3. If that works, try the launcher: python run_scripts.py")
    print("4. For Chrome driver issues, see TROUBLESHOOTING.md")

if __name__ == "__main__":
    main() 