"""
doc
"""
import os
import time
import pyautogui
import Xlib.display
from time import sleep
from selenium import webdriver
from pyvirtualdisplay.smartdisplay import SmartDisplay
display = SmartDisplay(visible=1, size=(1850, 1050))
display.start()

browser = webdriver.Chrome()
browser.get( 'https://www.make.com/en/login' )
browser.fullscreen_window()
browser.set_window_size(1850, 1050)
browser.save_screenshot( '1.png' )

# mouse moves in SmartDisplay 
pyautogui._pyautogui_x11._display = Xlib.display.Display(
     os.environ[ 'DISPLAY' ])
def detect_icon(icon_path: str):
    """
    Method take icon image path as input and detect it on browser to get its coordinates.

    Parameters
    ----------
    icon_path: str
        icon image path.

    Return
    ------
    None
    """
    image_coordinates = pyautogui.locateOnScreen(icon_path, confidence = 0.7)
    image_center_coordinates = pyautogui.center(image_coordinates)
    pyautogui.moveTo(image_center_coordinates[0], image_center_coordinates[1], 1)
    pyautogui.click(image_center_coordinates[0], image_center_coordinates[1])
    return image_coordinates

def login_via_bitwarden():
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
        time.sleep(2)
        pos = pyautogui.position()
        print(pos)
        time.sleep(2)

        # Locate the bitwarden icon to click
        cords_image = detect_icon("assets/bitwarden.png")
        if cords_image is not None:
            time.sleep(1)
        
        # Locate credentials in bitwarden
        cords_image_secret = detect_icon("assets/secret.png")
        if cords_image_secret is not None:
            time.sleep(1)

        # Locate the login button to click on it 
        cords_center_login = detect_icon("assets/login.png")
        if cords_center_login is not None:
            time.sleep(1)

        # Take a screenshot after the action
        screenshot = pyautogui.screenshot()
        screenshot.save('action_screenshot.png')

    except:
        # Take a screenshot after the action
        screenshot = pyautogui.screenshot()
        screenshot.save('action_screenshot.png')
        print("No Icon image found!")           

login_via_bitwarden()
browser.quit ( )
display.stop()
