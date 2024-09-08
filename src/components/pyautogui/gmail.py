"""
module to login to google account using bitwarden 
"""
import os
import time
import pyautogui
import Xlib.display
from openai import OpenAI
import undetected_chromedriver as uc

# from selenium.webdriver.chrome.service import Service # For Linux
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay.smartdisplay import SmartDisplay
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from dotenv import load_dotenv
from src.utils.helper_funtion import (
    check_unread_email,
    process_unread_emails,
    process_icon,
    show_custom_message,
    get_chrome_profile_path
)

from src.utils.helper.is_osx import is_osx

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
serp_api_key = os.getenv("SERPAPI_API_KEY")
model = OpenAI()
model.timeout = 10
BITWARDEN_EMAIL = os.getenv("BITWARDEN_EMAIL")
BITWARDEN_PASSWORD = os.getenv("BITWARDEN_PASSWORD")


async def login_via_bitwarden():
    try:
        # Create a ChromeOptions object
        chrome_options = uc.ChromeOptions()
        # Add the extension to ChromeOptions
        profile_path = get_chrome_profile_path()
        print(profile_path)
        if profile_path:
            user_profile_path = profile_path
        else:
            show_custom_message("Error Message", "Could not find the Chrome profile path.", duration = 3)
            return "Chrome Profile Path Error"

        chrome_options.add_argument('--no-default-browser-check')
        chrome_options.add_argument('--profile-directory=Default')
        chrome_options.add_argument("--load-extension=./src/Extensions/bitwarden")
        display = SmartDisplay(visible=1, size=(1850, 1050))
        display.start()

        #  For Linux add service=Service(ChromeDriverManager().install())
        browser = uc.Chrome(
            driver_executable_path=ChromeDriverManager(driver_version = "127.0.6533.72").install(),
            user_data_dir = user_profile_path,
            options= chrome_options,
            desired_capabilities=DesiredCapabilities.CHROME
            )
        browser.maximize_window()
        browser.save_screenshot("./src/components/pyautogui/screenshots/1.png")

        if not is_osx():
            # mouse moves in SmartDisplay
            pyautogui._pyautogui_x11._display = Xlib.display.Display(
                os.environ["DISPLAY"]
            )

        pos = pyautogui.position()
        print(pos)
        time.sleep(2)
        # Locate the Gmail icon on the main page to click on it
        cords_center_next = await process_icon("src/components/pyautogui/assets/move_to_inbox.png", 5)
        if cords_center_next is None:
            show_custom_message("Error Message", "Error during opening inbox.", duration = 2)
        time.sleep(10)

        # Check all unread emails
        unread_emails = check_unread_email(browser)
        if not unread_emails:
            browser.quit()
            display.stop()
            return "No unread emails"
        else:
            # Process each unread email
            unread_emails_response = process_unread_emails(browser, unread_emails)
            browser.quit()
            display.stop()
            return unread_emails_response
    except Exception as e:
        # Take a screenshot after the action
        screenshot = pyautogui.screenshot()
        screenshot.save("./src/components/pyautogui/screenshots/error_screenshot.png")
        show_custom_message("Error Message", "Something Went Wrong!", duration = 2)
        browser.quit()
        display.stop()
        return "Something Went Wrong!"


# print(login_via_bitwarden())
# browser.quit ()
# display.stop()
