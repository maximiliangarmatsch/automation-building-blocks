"""
module to login to google account using bitwarden 
"""
import os
import time
import asyncio
import pyautogui
import Xlib.display
from openai import OpenAI
from dotenv import load_dotenv
import undetected_chromedriver as uc
from pyvirtualdisplay.smartdisplay import SmartDisplay
from dotenv import load_dotenv
from utils.helper_funtion import detect_icon, check_unread_email, process_unread_emails

load_dotenv()
model = OpenAI()
model.timeout = 10
BITWARDEN_EMAIL = os.getenv("BITWARDEN_EMAIL")
BITWARDEN_PASSWORD = os.getenv("BITWARDEN_PASSWORD")

def detect_icon_with_retry(image_path, attempts=3, delay=2):
    """Try to detect the icon a specified number of times."""
    for attempt in range(attempts):
        cords = detect_icon(image_path)
        if cords is not None:
            return cords
        time.sleep(delay)
    return None

def process_icon(image_path, operation_delay):
    """Process each icon detection with error handling and custom delay."""
    cords = detect_icon_with_retry(image_path, attempts = 3, delay = operation_delay)
    if cords is not None:
        return cords
    else:
        return cords
def error_message(message, browser, display):
    """
    doc string
    """
    browser.quit ()
    display.stop() 
    return message
 
async def login_via_bitwarden():
    """
    login_via_bitwarden method will to the specific url and step by step perfomr action to login to make.com via bitwarden.

    Parameters
    ----------
    Nooe

    Return
    ------
    None
    """
    try:
        # Create a ChromeOptions object
        chrome_options = uc.ChromeOptions()
        # global chrome_options
        # Add the extension to ChromeOptions
        chrome_options.add_argument('--load-extension=./Extensions/bitwarden')
        display = SmartDisplay(visible = 1, size=(1850, 1050))
        display.start()

        browser = uc.Chrome(options=chrome_options)
        browser.get('https://accounts.google.com/AccountChooser?service=mail&continue=https://google.com&hl=en')
        browser.maximize_window()
        browser.save_screenshot( '1.png' )

        # mouse moves in SmartDisplay 
        pyautogui._pyautogui_x11._display = Xlib.display.Display(
            os.environ[ 'DISPLAY' ])
        pos = pyautogui.position()
        print(pos)
        time.sleep(2)

        # Locate the extensions icon to click
        cords_image = process_icon("assets/extension.png", 2)
        if cords_image is None:
            return error_message("Error While click on Extensions Icon", browser, display)

        # Locate the pin extension to taskbar icon to click
        cords_image_pin = process_icon("assets/pins.png", 1)
        if cords_image_pin is None:
            return error_message("Error while Pin Bitarden extension.", browser, display)
        
        # # Locate the Bitwarden extension on the taskbar icon to click
        # cords_image_before_login = process_icon("assets/bitwarden_before_login.png", 5)
        # print(cords_image_before_login)
        # if cords_image_before_login is None:
        #     return error_message("Error While Click on Bitwarden.", browser, display)
        time.sleep(2)
        image_coordinates = pyautogui.locateOnScreen("assets/bitwarden_before_login.png", confidence = 0.6)
        image_center_coordinates = pyautogui.center(image_coordinates)
        pyautogui.moveTo(image_center_coordinates[0], image_center_coordinates[1], 1)
        pyautogui.click(image_center_coordinates[0], image_center_coordinates[1])

        # Locate the Bitwarden email text field icon to click
        cords_image_enter_gmail = process_icon("assets/enter_gmail.png", 1)
        if cords_image_enter_gmail is not None:
            pyautogui.typewrite(BITWARDEN_EMAIL)
        
        # Locate the Bitwarden continue icon to click
        cords_image_gmail_continue = process_icon("assets/gmail_continue.png", 2)
        if cords_image_gmail_continue is not None:
            pyautogui.typewrite(BITWARDEN_PASSWORD)

        # Locate the Bitwarden master login icon to click
        cords_image_master_password_login = process_icon("assets/master_password_login.png", 2)
        if cords_image_master_password_login is None:
            return error_message("Error during bitwarden login.", browser, display)
        
        # Locate any random position to click
        cords_image_random = process_icon("assets/gmail_random.png", 5)
        if cords_image_random is None:
            return error_message("Random position icon not found.", browser, display)
        
        # Locate the Bitwarden icon to click
        cords_image_bitwarden = process_icon("assets/bitwardens.png", 2)
        if cords_image_bitwarden is None:
            return error_message("Bitwarden icon not found.", browser, display)
        
        # Locate credentials in Bitwarden
        cords_image_gmail = process_icon("assets/select_asim_gmail.png", 2)
        if cords_image_gmail is None:
            return error_message("Mentioed Gmail not found.", browser, display)
        
        # Locate any random position to click
        cords_image_random = process_icon("assets/signin_random.png", 1)
        if cords_image_random is None:
            return error_message("Signin random icon not found.", browser, display)
        
        # Locate the login button to click on it
        cords_center_next = process_icon("assets/gmail_next.png", 2)
        if cords_center_next is None:
            return error_message("Error while login to google account.", browser, display)
        
        # Locate the Bitwarden icon to click
        cords_image_bitwarden = process_icon("assets/bitwardens.png", 2)
        if cords_image_bitwarden is None:
            return error_message("Bitwarden icon not found.", browser, display)
        
        # Locate credentials in Bitwarden
        cords_image_password = process_icon("assets/select_asim_gmail.png", 2)
        if cords_image_password is None:
            return error_message("Mentioed Gmail not found.", browser, display)
        
        # Locate the login button to click on it
        cords_center_next = process_icon("assets/gmail_next.png", 5)
        if cords_center_next is None:
            return error_message("Error while login to Gmails account.", browser, display)
        
        # Locate the Gmail icon on the main page to click on it
        cords_center_next = process_icon("assets/move_to_inbox.png", 5)
        if cords_center_next is None:
            return error_message("Erro during open gmail inbox.", browser, display)
    
        # Check all unread emails 
        unread_emails = check_unread_email(browser)
        if not unread_emails:
            browser.quit ()
            display.stop()
            return "No unread emails"
        else:
            # Process each unread email 
            unread_emails_response = process_unread_emails(browser, unread_emails)
            browser.quit ()
            display.stop()
            return unread_emails_response
    except:
        # Take a screenshot after the action
        screenshot = pyautogui.screenshot()
        screenshot.save('error_screenshot.png')
        print("Error during Crawling!")    
        browser.quit ()
        display.stop()     
        return "Something Went Wrong!"   

# print(login_via_bitwarden())
# browser.quit ()
# display.stop()