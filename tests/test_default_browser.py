from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
# How to get default browser path on Windows, macOS, Ubantu

# On Windows: C:\Users\<YourUsername>\AppData\Local\Google\Chrome\User Data
# On macOS: /Users/<YourUsername>/Library/Application Support/Google/Chrome
# On Ubuntu/Linux: /home/<YourUsername>/.config/google-chrome

import undetected_chromedriver as uc
options = uc.ChromeOptions()
user_data_dir = '/home/aamir/.config/google-chrome/Default'
options.add_argument('--no-default-browser-check')
options.add_argument('--profile-directory=Default')
options.add_argument("--load-extension=./src/Extensions/bitwarden")

browser = uc.Chrome(
    driver_executable_path=ChromeDriverManager(driver_version = "127.0.6533.72").install(),
    user_data_dir = user_data_dir,
    options= options,
    desired_capabilities=DesiredCapabilities.CHROME
    )
time.sleep(6)
browser.get("https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox")
time.sleep(20)
