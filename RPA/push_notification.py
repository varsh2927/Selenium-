from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()

# Use a working demo login site
driver.get("https://the-internet.herokuapp.com/login")
time.sleep(2)

# Sample login
driver.find_element(By.ID, "username").send_keys("tomsmith")
driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
driver.find_element(By.CSS_SELECTOR, "button.radius").click()

print("Logged in successfully.")
time.sleep(5)
driver.quit()
