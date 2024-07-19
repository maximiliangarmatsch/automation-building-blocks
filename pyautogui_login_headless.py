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
try:
    time.sleep(5)
    pos = pyautogui.position()
    print(pos)
    time.sleep(4)
    # Locate the image on the screen with a confidence threshold
    cords_image = pyautogui.locateOnScreen('assets/bitwarden.png', confidence = 0.7)
    if cords_image is not None:
        cords_center = pyautogui.center(cords_image) # Find the center of detected icon
        pyautogui.moveTo(cords_center[0], cords_center[1], 1) # Move mouse to specified position
        pyautogui.click(cords_center[0], cords_center[1]) # Click on the located image
        time.sleep(2) # Wait a bit to ensure the click action is registered
        
        cords_image_secret = pyautogui.locateOnScreen('assets/secret.png', confidence = 0.7)
        cords_center_secret = pyautogui.center(cords_image_secret) # Find the center of detected icon
        pyautogui.moveTo(cords_center_secret[0], cords_center_secret[1], 1) # Move mouse to specified position
        pyautogui.click(cords_center_secret[0], cords_center_secret[1]) # Click on the located image
        time.sleep(2) # Wait a bit to ensure the click action is registered

        cords_image_login = pyautogui.locateOnScreen('assets/login.png', confidence = 0.7)
        cords_center_login = pyautogui.center(cords_image_login) # Find the center of detected icon
        pyautogui.moveTo(cords_center_login[0], cords_center_login[1], 1) # Move mouse to specified position
        pyautogui.click(cords_center_login[0], cords_center_login[1]) # Click on the located image
        time.sleep(2) # Wait a bit to ensure the click action is registered

        # Take a screenshot after the action
        screenshot = pyautogui.screenshot()
        screenshot.save('action_screenshot.png')

        # Print the coordinates of the image and center
        print(cords_image, cords_center)
except:
    # Take a screenshot after the action
    screenshot = pyautogui.screenshot()
    screenshot.save('action_screenshot.png')
    print("no magnifier found!")           

sleep(3)
browser.quit ( )
display.stop()
