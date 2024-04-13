from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome webdriver
driver = webdriver.Chrome()

# Open the webpage
driver.get('https://www.cars24.com/rto-vehicle-registration-details/')

# Find the input element and set its value
input_element = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.form-control')))
input_element.send_keys('HR26AU0637')  # Set the value of the input field

buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'button._2iiQB._3qpfi')))

# Click the second button
buttons[1].click()

WebDriverWait(driver, 10).until(EC.url_changes(driver.current_url))

# Now you can access the new URL
new_url = driver.current_url
print("Next page URL:", new_url)

element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'some_element_selector')))
element.click() 