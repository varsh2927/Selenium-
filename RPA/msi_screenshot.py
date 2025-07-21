from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# ✅ Tell Selenium where to find your Chrome browser
chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

# Automatically download the right chromedriver
service = Service(ChromeDriverManager().install())

# Launch browser
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open MSI store
driver.get("https://www.msi.com/")

# Wait for page to load
time.sleep(5)

# Take screenshot
driver.save_screenshot("msi_screenshot.png")
print("Screenshot saved as msi_screenshot.png")

# Close browser
driver.quit()
