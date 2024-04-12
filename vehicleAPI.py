from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the Chrome webdriver
driver = webdriver.Chrome()

# Open the webpage
driver.get('https://www.cars24.com/rto-vehicle-registration-details/')

try:
    # Find the input element and set its value
    input_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.form-control')))
    input_element.send_keys('HR26AU0637')  # Set the value of the input field

    # Find and click the button
    button_element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button._2iiQB._3qpfi')))
    button_element.click()

    # Wait for the next page to load
    WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))

    # Now you can access the new URL
    new_url = driver.current_url
    print("Next page URL:", new_url)

except Exception as e:
    print("An error occurred:", e)

finally:
    # Close the browser
    driver.quit()
