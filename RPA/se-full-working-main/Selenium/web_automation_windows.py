"""
Web Automation Script for Windows using Selenium
This script is specifically designed to handle Windows-specific Chrome driver issues.
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Try to import Selenium components
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    print("✅ Selenium imports successful")
except ImportError as e:
    print(f"❌ Selenium import error: {e}")
    sys.exit(1)

class WindowsWebAutomation:
    def __init__(self, headless=True):
        """Initialize web automation with Windows-specific settings"""
        self.driver = None
        self.wait = None
        self.setup_driver(headless)
    
    def setup_driver(self, headless=True):
        """Set up Chrome driver with Windows-specific configurations"""
        print("Setting up Chrome driver for Windows...")
        
        # Chrome options for Windows
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless=new")  # Use new headless mode
        
        # Windows-specific arguments
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Method 1: Try with webdriver-manager
            print("Attempting to use webdriver-manager...")
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                print("✅ Chrome driver initialized with webdriver-manager")
            except Exception as e1:
                print(f"webdriver-manager failed: {e1}")
                
                # Method 2: Try without service (let Selenium find driver)
                print("Trying without explicit service...")
                try:
                    self.driver = webdriver.Chrome(options=chrome_options)
                    print("✅ Chrome driver initialized without service")
                except Exception as e2:
                    print(f"Direct Chrome initialization failed: {e2}")
                    
                    # Method 3: Try with system PATH
                    print("Trying with system PATH...")
                    try:
                        # Check if chromedriver is in PATH
                        result = subprocess.run(['chromedriver', '--version'], 
                                              capture_output=True, text=True)
                        if result.returncode == 0:
                            print("ChromeDriver found in PATH")
                            self.driver = webdriver.Chrome(options=chrome_options)
                            print("✅ Chrome driver initialized from PATH")
                        else:
                            raise Exception("ChromeDriver not found in PATH")
                    except Exception as e3:
                        print(f"PATH method failed: {e3}")
                        raise Exception("All Chrome driver initialization methods failed")
            
            # Set up wait
            self.wait = WebDriverWait(self.driver, 10)
            print("✅ WebDriver setup completed successfully!")
            
        except Exception as e:
            print(f"❌ Failed to initialize Chrome driver: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure Google Chrome is installed and up to date")
            print("2. Try running: pip install --upgrade webdriver-manager")
            print("3. Download ChromeDriver manually from: https://chromedriver.chromium.org/")
            print("4. Add ChromeDriver to your system PATH")
            raise
    
    def navigate_to_website(self, url):
        """Navigate to a website"""
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            print(f"✅ Successfully navigated to: {url}")
            return True
        except Exception as e:
            print(f"❌ Error navigating to {url}: {e}")
            return False
    
    def take_screenshot(self, filename=None):
        """Take a screenshot"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            print(f"✅ Screenshot saved: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return None
    
    def get_page_title(self):
        """Get the current page title"""
        try:
            title = self.driver.title
            print(f"Page title: {title}")
            return title
        except Exception as e:
            print(f"❌ Error getting page title: {e}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                print("✅ Browser closed successfully")
            except Exception as e:
                print(f"❌ Error closing browser: {e}")

def test_basic_functionality():
    """Test basic web automation functionality"""
    print("=" * 60)
    print("Testing Basic Web Automation Functionality")
    print("=" * 60)
    
    automation = None
    try:
        # Initialize automation
        automation = WindowsWebAutomation(headless=True)
        
        # Test 1: Navigate to a simple website
        print("\n--- Test 1: Basic Navigation ---")
        success = automation.navigate_to_website("https://httpbin.org/get")
        if success:
            title = automation.get_page_title()
            automation.take_screenshot("test_httpbin.png")
        
        # Test 2: Navigate to Google (more complex)
        print("\n--- Test 2: Google Navigation ---")
        success = automation.navigate_to_website("https://www.google.com")
        if success:
            title = automation.get_page_title()
            automation.take_screenshot("test_google.png")
        
        # Test 3: Navigate to Python.org
        print("\n--- Test 3: Python.org Navigation ---")
        success = automation.navigate_to_website("https://www.python.org")
        if success:
            title = automation.get_page_title()
            automation.take_screenshot("test_python.png")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        print("\nThis might be due to:")
        print("- Chrome browser not installed")
        print("- Chrome version mismatch")
        print("- Windows security settings")
        print("- Network connectivity issues")
    
    finally:
        if automation:
            automation.close()

def main():
    """Main function"""
    print("🚀 Windows Web Automation Test")
    print("This script tests basic web automation functionality on Windows.")
    
    # Check if we're on Windows
    if os.name != 'nt':
        print("⚠️  This script is designed for Windows. Running on other platforms may cause issues.")
    
    # Run the test
    test_basic_functionality()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    main() 