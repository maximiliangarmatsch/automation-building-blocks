import time

import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()

# normally most chrome chrome functionality would work fine, even without a display,
# as long as we start it with the "headless" option. But to confirm the virtual display works,
# we'll omit the headless option
#
# options.add_argument("--headless")

options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


try:
    driver = webdriver.Chrome(options=options)
    # Navigate to a website
    driver.get("https://www.example.com")

    # Wait for page to load
    time.sleep(5)

    # Perform PyAutoGUI actions
    pyautogui.moveTo(100, 100)
    pos = pyautogui.position()
    print("POSITION ", pos)
    pyautogui.click()

    # Take a screenshot
    pyautogui.screenshot("screenshots/screenshot.png")

    print("Actions completed successfully")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Clean up
    driver.quit()
