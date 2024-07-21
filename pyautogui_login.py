"""
Main module to automate the screen reading using pyautogui
"""
import time
import webbrowser
import pyautogui

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
        webbrowser.open("https://www.make.com/en/login")
        time.sleep(2)
        pos = pyautogui.position()
        print(pos)
        time.sleep(2)
        # Locate the image on the screen with a confidence threshold
        cords_image = pyautogui.locateOnScreen('assets/bitwarden.png', confidence = 0.7)
        if cords_image is not None:
            cords_center = pyautogui.center(cords_image) # Find the center of detected icon
            pyautogui.moveTo(cords_center[0], cords_center[1], 1) # Move mouse to specified position
            pyautogui.click(cords_center[0], cords_center[1]) # Click on the located image
            time.sleep(1) # Wait a bit to ensure the click action is registered
            
            cords_image_secret = pyautogui.locateOnScreen('assets/secret.png', confidence = 0.7)
            cords_center_secret = pyautogui.center(cords_image_secret) # Find the center of detected icon
            pyautogui.moveTo(cords_center_secret[0], cords_center_secret[1], 1) # Move mouse to specified position
            pyautogui.click(cords_center_secret[0], cords_center_secret[1]) # Click on the located image
            time.sleep(1) # Wait a bit to ensure the click action is registered

            cords_image_login = pyautogui.locateOnScreen('assets/login.png', confidence = 0.7)
            cords_center_login = pyautogui.center(cords_image_login) # Find the center of detected icon
            pyautogui.moveTo(cords_center_login[0], cords_center_login[1], 1) # Move mouse to specified position
            pyautogui.click(cords_center_login[0], cords_center_login[1]) # Click on the located image
            time.sleep(1) # Wait a bit to ensure the click action is registered

            # Take a screenshot after the action
            screenshot = pyautogui.screenshot()
            screenshot.save('action_screenshot.png')

            # Print the coordinates of the image and center
            print(cords_image, cords_center)
        else:
            print("Image not found on the screen")
    except pyautogui.ImageNotFoundException:
        print("Image not found exception occurred")

login_via_bitwarden()
