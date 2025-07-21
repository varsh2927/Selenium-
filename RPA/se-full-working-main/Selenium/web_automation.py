"""
Web Automation Script using Selenium
This script demonstrates various web automation tasks including:
- Form filling and submission
- Navigation and clicking
- Data extraction
- Screenshot capture
- Handling dynamic content
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import sys
from datetime import datetime

class WebAutomation:
    def __init__(self, headless=False):
        """Initialize the web automation with Chrome driver"""
        self.chrome_options = Options()
        if headless:
            self.chrome_options.add_argument("--headless")
        
        # Windows-specific options
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--window-size=1920,1080")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-plugins")
        self.chrome_options.add_argument("--disable-images")
        self.chrome_options.add_argument("--disable-javascript")  # Only if needed
        self.chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Add user agent to avoid detection
        self.chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Initialize driver with automatic ChromeDriver management
            print("Setting up Chrome driver...")
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome driver initialized successfully!")
        except Exception as e:
            print(f"Error initializing Chrome driver: {e}")
            print("Trying alternative approach...")
            try:
                # Alternative approach without webdriver-manager
                self.driver = webdriver.Chrome(options=self.chrome_options)
                self.wait = WebDriverWait(self.driver, 10)
                print("Chrome driver initialized with alternative approach!")
            except Exception as e2:
                print(f"Failed to initialize Chrome driver: {e2}")
                print("Please make sure Chrome browser is installed and up to date.")
                raise
        
    def navigate_to_website(self, url):
        """Navigate to a specific website"""
        try:
            print(f"Navigating to: {url}")
            self.driver.get(url)
            print(f"Successfully navigated to: {url}")
            return True
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            return False
    
    def fill_form(self, form_data):
        """Fill out a form with provided data"""
        try:
            # Example: Filling out a contact form
            for field_name, value in form_data.items():
                try:
                    element = self.wait.until(
                        EC.presence_of_element_located((By.NAME, field_name))
                    )
                    element.clear()
                    element.send_keys(value)
                    print(f"Filled {field_name}: {value}")
                except Exception as e:
                    print(f"Could not fill {field_name}: {e}")
            return True
        except Exception as e:
            print(f"Error filling form: {e}")
            return False
    
    def click_element(self, by, value):
        """Click on an element"""
        try:
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            element.click()
            print(f"Clicked element: {value}")
            return True
        except Exception as e:
            print(f"Error clicking element {value}: {e}")
            return False
    
    def extract_data(self, selectors):
        """Extract data from web elements"""
        data = {}
        try:
            for key, selector in selectors.items():
                try:
                    element = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    data[key] = element.text
                    print(f"Extracted {key}: {element.text}")
                except Exception as e:
                    print(f"Could not extract {key}: {e}")
            return data
        except Exception as e:
            print(f"Error extracting data: {e}")
            return data
    
    def take_screenshot(self, filename=None):
        """Take a screenshot of the current page"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            print(f"Screenshot saved as: {filename}")
            return filename
        except Exception as e:
            print(f"Error taking screenshot: {e}")
            return None
    
    def scroll_page(self, direction="down"):
        """Scroll the page up or down"""
        try:
            if direction == "down":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            elif direction == "up":
                self.driver.execute_script("window.scrollTo(0, 0);")
            print(f"Scrolled page {direction}")
            time.sleep(2)
        except Exception as e:
            print(f"Error scrolling page: {e}")
    
    def wait_for_element(self, by, value, timeout=10):
        """Wait for an element to be present"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"Element found: {value}")
            return element
        except Exception as e:
            print(f"Element not found: {value}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("Browser closed")

def main():
    """Main function demonstrating web automation"""
    print("Starting Web Automation Demo...")
    
    try:
        automation = WebAutomation(headless=False)
        
        # Example 1: Google Search Automation
        print("\n=== Google Search Automation ===")
        automation.navigate_to_website("https://www.google.com")
        
        # Accept cookies if present
        try:
            automation.click_element(By.XPATH, "//button[contains(text(), 'Accept all')]")
        except:
            print("No cookie consent found or already accepted")
        
        # Perform search
        search_box = automation.wait_for_element(By.NAME, "q")
        if search_box:
            search_box.send_keys("Python Selenium automation")
            search_box.send_keys(Keys.RETURN)
            time.sleep(3)
            
            # Extract search results
            results = automation.extract_data({
                "first_result": "h3",
                "result_count": "#result-stats"
            })
            
            # Take screenshot
            automation.take_screenshot("google_search_results.png")
        
        # Example 2: Form Automation (using a test site)
        print("\n=== Form Automation Example ===")
        automation.navigate_to_website("https://httpbin.org/forms/post")
        
        # Fill form data
        form_data = {
            "custname": "John Doe",
            "custtel": "123-456-7890",
            "custemail": "john@example.com",
            "size": "large",
            "topping": "bacon",
            "delivery": "20:00",
            "comments": "Please deliver quickly!"
        }
        
        automation.fill_form(form_data)
        
        # Example 3: Navigation and Interaction
        print("\n=== Navigation Example ===")
        automation.navigate_to_website("https://www.python.org")
        
        # Click on different sections
        automation.click_element(By.LINK_TEXT, "Downloads")
        time.sleep(2)
        
        automation.click_element(By.LINK_TEXT, "Documentation")
        time.sleep(2)
        
        # Scroll and take screenshot
        automation.scroll_page("down")
        automation.take_screenshot("python_org.png")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        print("This might be due to Chrome browser issues or network connectivity.")
    
    finally:
        try:
            automation.close()
        except:
            pass
        print("Web automation demo completed.")

if __name__ == "__main__":
    main() 