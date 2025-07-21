"""
Web Testing Script using Selenium and Pytest
This script demonstrates various web testing techniques including:
- Functional testing
- UI/UX testing
- Performance testing
- Cross-browser testing
- Automated test reporting
- Test data management
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import time
import json
import os
from datetime import datetime
import logging
from typing import Dict, List, Any
import requests
from dataclasses import dataclass

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Data class for storing test results"""
    test_name: str
    status: str  # 'PASS', 'FAIL', 'SKIP'
    duration: float
    error_message: str = ""
    screenshot_path: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class WebTestBase:
    """Base class for web testing"""
    
    def __init__(self, browser="chrome", headless=True):
        """Initialize the web test base"""
        self.browser = browser.lower()
        self.headless = headless
        self.driver = None
        self.wait = None
        self.test_results = []
        
    def setup_driver(self):
        """Set up the web driver"""
        try:
            if self.browser == "chrome":
                chrome_options = Options()
                if self.headless:
                    chrome_options.add_argument("--headless")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                
            elif self.browser == "firefox":
                firefox_options = FirefoxOptions()
                if self.headless:
                    firefox_options.add_argument("--headless")
                
                service = Service(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=firefox_options)
            
            self.wait = WebDriverWait(self.driver, 10)
            logger.info(f"Driver initialized for {self.browser}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up driver: {e}")
            return False
    
    def teardown_driver(self):
        """Tear down the web driver"""
        if self.driver:
            self.driver.quit()
            logger.info("Driver closed")
    
    def take_screenshot(self, test_name):
        """Take a screenshot"""
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{test_name}_{timestamp}.png"
        
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"Screenshot saved: {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return ""
    
    def record_test_result(self, test_name, status, duration, error_message="", screenshot_path=""):
        """Record test result"""
        result = TestResult(
            test_name=test_name,
            status=status,
            duration=duration,
            error_message=error_message,
            screenshot_path=screenshot_path
        )
        self.test_results.append(result)
        logger.info(f"Test {test_name}: {status}")

class FunctionalTestSuite(WebTestBase):
    """Functional testing suite"""
    
    def test_google_search(self):
        """Test Google search functionality"""
        test_name = "test_google_search"
        start_time = time.time()
        
        try:
            # Navigate to Google
            self.driver.get("https://www.google.com")
            
            # Accept cookies if present
            try:
                accept_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept all')]")))
                accept_button.click()
            except:
                pass
            
            # Find search box and enter query
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "q")))
            search_box.send_keys("Python Selenium testing")
            search_box.send_keys(Keys.RETURN)
            
            # Wait for results
            self.wait.until(EC.presence_of_element_located((By.ID, "search")))
            
            # Verify search results are present
            results = self.driver.find_elements(By.CSS_SELECTOR, "h3")
            assert len(results) > 0, "No search results found"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise
    
    def test_form_submission(self):
        """Test form submission functionality"""
        test_name = "test_form_submission"
        start_time = time.time()
        
        try:
            # Navigate to test form
            self.driver.get("https://httpbin.org/forms/post")
            
            # Fill form fields
            form_data = {
                "custname": "Test User",
                "custtel": "123-456-7890",
                "custemail": "test@example.com",
                "size": "large",
                "topping": "bacon",
                "delivery": "20:00",
                "comments": "Automated test submission"
            }
            
            for field_name, value in form_data.items():
                field = self.wait.until(EC.presence_of_element_located((By.NAME, field_name)))
                field.clear()
                field.send_keys(value)
            
            # Submit form
            submit_button = self.driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
            submit_button.click()
            
            # Verify submission (check for success page or redirect)
            time.sleep(2)
            current_url = self.driver.current_url
            assert "httpbin.org" in current_url, "Form submission failed"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise
    
    def test_navigation(self):
        """Test website navigation"""
        test_name = "test_navigation"
        start_time = time.time()
        
        try:
            # Navigate to Python.org
            self.driver.get("https://www.python.org")
            
            # Test navigation to Downloads page
            downloads_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Downloads")))
            downloads_link.click()
            
            # Verify we're on downloads page
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
            assert "Downloads" in self.driver.title, "Navigation to Downloads failed"
            
            # Test navigation to Documentation
            doc_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Documentation")))
            doc_link.click()
            
            # Verify we're on documentation page
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
            assert "Documentation" in self.driver.title, "Navigation to Documentation failed"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise

class UITestSuite(WebTestBase):
    """UI/UX testing suite"""
    
    def test_responsive_design(self):
        """Test responsive design at different screen sizes"""
        test_name = "test_responsive_design"
        start_time = time.time()
        
        try:
            # Test different screen sizes
            screen_sizes = [
                (1920, 1080),  # Desktop
                (1366, 768),   # Laptop
                (768, 1024),   # Tablet
                (375, 667)     # Mobile
            ]
            
            self.driver.get("https://www.python.org")
            
            for width, height in screen_sizes:
                self.driver.set_window_size(width, height)
                time.sleep(2)
                
                # Check if page loads properly
                assert self.driver.find_element(By.TAG_NAME, "body"), f"Page not loading at {width}x{height}"
                
                # Take screenshot for visual verification
                self.take_screenshot(f"responsive_{width}x{height}")
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise
    
    def test_element_visibility(self):
        """Test element visibility and accessibility"""
        test_name = "test_element_visibility"
        start_time = time.time()
        
        try:
            self.driver.get("https://www.python.org")
            
            # Test if key elements are visible
            key_elements = [
                (By.CSS_SELECTOR, "header"),
                (By.CSS_SELECTOR, "nav"),
                (By.CSS_SELECTOR, "main"),
                (By.LINK_TEXT, "Downloads"),
                (By.LINK_TEXT, "Documentation")
            ]
            
            for by, selector in key_elements:
                element = self.wait.until(EC.visibility_of_element_located((by, selector)))
                assert element.is_displayed(), f"Element {selector} is not visible"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise
    
    def test_page_load_time(self):
        """Test page load performance"""
        test_name = "test_page_load_time"
        start_time = time.time()
        
        try:
            # Measure page load time
            page_start = time.time()
            self.driver.get("https://www.python.org")
            
            # Wait for page to be fully loaded
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            
            page_load_time = time.time() - page_start
            
            # Assert page loads within reasonable time (5 seconds)
            assert page_load_time < 5.0, f"Page load time {page_load_time:.2f}s exceeds 5 seconds"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise

class PerformanceTestSuite(WebTestBase):
    """Performance testing suite"""
    
    def test_api_response_time(self):
        """Test API response times"""
        test_name = "test_api_response_time"
        start_time = time.time()
        
        try:
            # Test various API endpoints
            api_endpoints = [
                "https://httpbin.org/get",
                "https://httpbin.org/post",
                "https://httpbin.org/json",
                "https://httpbin.org/xml"
            ]
            
            for endpoint in api_endpoints:
                api_start = time.time()
                response = requests.get(endpoint, timeout=10)
                api_response_time = time.time() - api_start
                
                assert response.status_code == 200, f"API {endpoint} returned {response.status_code}"
                assert api_response_time < 2.0, f"API {endpoint} response time {api_response_time:.2f}s exceeds 2 seconds"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            self.record_test_result(test_name, "FAIL", duration, str(e))
            raise
    
    def test_concurrent_users(self):
        """Simulate concurrent user testing"""
        test_name = "test_concurrent_users"
        start_time = time.time()
        
        try:
            # This is a simplified version - in real scenarios you'd use tools like JMeter
            # Here we just test multiple rapid requests
            self.driver.get("https://www.python.org")
            
            # Simulate multiple page loads
            for i in range(5):
                self.driver.refresh()
                time.sleep(0.5)
                
                # Verify page still loads correctly
                assert self.driver.find_element(By.TAG_NAME, "body"), f"Page failed to load on refresh {i+1}"
            
            duration = time.time() - start_time
            self.record_test_result(test_name, "PASS", duration)
            
        except Exception as e:
            duration = time.time() - start_time
            screenshot_path = self.take_screenshot(test_name)
            self.record_test_result(test_name, "FAIL", duration, str(e), screenshot_path)
            raise

class TestReporter:
    """Test reporting and results management"""
    
    def __init__(self):
        self.results = []
    
    def add_results(self, test_results: List[TestResult]):
        """Add test results to the reporter"""
        self.results.extend(test_results)
    
    def generate_html_report(self, filename="test_report.html"):
        """Generate HTML test report"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Web Test Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #f0f0f0; padding: 20px; border-radius: 5px; }
                .summary { margin: 20px 0; }
                .test-result { margin: 10px 0; padding: 10px; border-radius: 5px; }
                .pass { background-color: #d4edda; border: 1px solid #c3e6cb; }
                .fail { background-color: #f8d7da; border: 1px solid #f5c6cb; }
                .skip { background-color: #fff3cd; border: 1px solid #ffeaa7; }
                .screenshot { max-width: 300px; margin: 10px 0; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Web Test Report</h1>
                <p>Generated on: {timestamp}</p>
            </div>
        """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Add summary
        total_tests = len(self.results)
        passed_tests = len([r for r in self.results if r.status == "PASS"])
        failed_tests = len([r for r in self.results if r.status == "FAIL"])
        skipped_tests = len([r for r in self.results if r.status == "SKIP"])
        
        html_content += f"""
            <div class="summary">
                <h2>Test Summary</h2>
                <p><strong>Total Tests:</strong> {total_tests}</p>
                <p><strong>Passed:</strong> {passed_tests}</p>
                <p><strong>Failed:</strong> {failed_tests}</p>
                <p><strong>Skipped:</strong> {skipped_tests}</p>
                <p><strong>Success Rate:</strong> {(passed_tests/total_tests*100):.1f}%</p>
            </div>
        """
        
        # Add individual test results
        html_content += "<h2>Test Results</h2>"
        for result in self.results:
            status_class = result.status.lower()
            html_content += f"""
                <div class="test-result {status_class}">
                    <h3>{result.test_name}</h3>
                    <p><strong>Status:</strong> {result.status}</p>
                    <p><strong>Duration:</strong> {result.duration:.2f}s</p>
                    <p><strong>Timestamp:</strong> {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
            """
            
            if result.error_message:
                html_content += f"<p><strong>Error:</strong> {result.error_message}</p>"
            
            if result.screenshot_path and os.path.exists(result.screenshot_path):
                html_content += f'<img src="{result.screenshot_path}" class="screenshot" alt="Test Screenshot">'
            
            html_content += "</div>"
        
        html_content += "</body></html>"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {filename}")
    
    def generate_json_report(self, filename="test_report.json"):
        """Generate JSON test report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(self.results),
                "passed": len([r for r in self.results if r.status == "PASS"]),
                "failed": len([r for r in self.results if r.status == "FAIL"]),
                "skipped": len([r for r in self.results if r.status == "SKIP"])
            },
            "results": [
                {
                    "test_name": r.test_name,
                    "status": r.status,
                    "duration": r.duration,
                    "error_message": r.error_message,
                    "screenshot_path": r.screenshot_path,
                    "timestamp": r.timestamp.isoformat()
                }
                for r in self.results
            ]
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"JSON report generated: {filename}")

def run_all_tests():
    """Run all test suites"""
    reporter = TestReporter()
    
    # Run functional tests
    print("Running Functional Tests...")
    functional_tests = FunctionalTestSuite(browser="chrome", headless=True)
    if functional_tests.setup_driver():
        try:
            functional_tests.test_google_search()
            functional_tests.test_form_submission()
            functional_tests.test_navigation()
        finally:
            functional_tests.teardown_driver()
            reporter.add_results(functional_tests.test_results)
    
    # Run UI tests
    print("Running UI Tests...")
    ui_tests = UITestSuite(browser="chrome", headless=True)
    if ui_tests.setup_driver():
        try:
            ui_tests.test_responsive_design()
            ui_tests.test_element_visibility()
            ui_tests.test_page_load_time()
        finally:
            ui_tests.teardown_driver()
            reporter.add_results(ui_tests.test_results)
    
    # Run performance tests
    print("Running Performance Tests...")
    performance_tests = PerformanceTestSuite(browser="chrome", headless=True)
    if performance_tests.setup_driver():
        try:
            performance_tests.test_api_response_time()
            performance_tests.test_concurrent_users()
        finally:
            performance_tests.teardown_driver()
            reporter.add_results(performance_tests.test_results)
    
    # Generate reports
    reporter.generate_html_report()
    reporter.generate_json_report()
    
    print("All tests completed. Check test_report.html and test_report.json for results.")

if __name__ == "__main__":
    run_all_tests() 