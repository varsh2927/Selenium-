#!/usr/bin/env python3
"""
Simple test script to verify Selenium setup on Windows
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import selenium
        print("✅ Selenium imported successfully")
    except ImportError as e:
        print(f"❌ Selenium import failed: {e}")
        return False
    
    try:
        from selenium import webdriver
        print("✅ Selenium webdriver imported successfully")
    except ImportError as e:
        print(f"❌ Selenium webdriver import failed: {e}")
        return False
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✅ WebDriver Manager imported successfully")
    except ImportError as e:
        print(f"❌ WebDriver Manager import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ Requests imported successfully")
    except ImportError as e:
        print(f"❌ Requests import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup imported successfully")
    except ImportError as e:
        print(f"❌ BeautifulSoup import failed: {e}")
        return False
    
    return True

def test_chrome_driver():
    """Test Chrome driver setup"""
    print("\nTesting Chrome driver setup...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        print("Downloading Chrome driver...")
        service = Service(ChromeDriverManager().install())
        
        print("Initializing Chrome driver...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("Testing navigation...")
        driver.get("https://www.google.com")
        
        print(f"Page title: {driver.title}")
        
        driver.quit()
        print("✅ Chrome driver test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Chrome driver test failed: {e}")
        return False

def test_basic_requests():
    """Test basic HTTP requests"""
    print("\nTesting HTTP requests...")
    
    try:
        import requests
        
        response = requests.get("https://httpbin.org/get", timeout=10)
        print(f"✅ HTTP request successful: Status {response.status_code}")
        return True
        
    except Exception as e:
        print(f"❌ HTTP request failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 50)
    print("Selenium Setup Test for Windows")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check your installation.")
        return
    
    # Test HTTP requests
    if not test_basic_requests():
        print("\n❌ HTTP request test failed. Check your internet connection.")
        return
    
    # Test Chrome driver (this might fail on some systems)
    try:
        test_chrome_driver()
    except Exception as e:
        print(f"\n⚠️  Chrome driver test failed: {e}")
        print("This is common on Windows. You may need to:")
        print("1. Install Google Chrome browser")
        print("2. Update Chrome to the latest version")
        print("3. Check Windows Defender/firewall settings")
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main() 