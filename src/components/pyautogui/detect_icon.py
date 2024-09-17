import time
import pyautogui
from utils.helper.is_osx import is_osx


def detect_icon_with_retry(image_path, attempts=3, delay=2):
    for attempt in range(attempts):
        cords = detect_icon(image_path)
        if cords is not None:
            return cords
        print(f"No of attemps: {attempt}")
        time.sleep(delay)
    return None


def detect_icon(icon_path: str):
    image_coordinates = None
    image_coordinates = pyautogui.locateOnScreen(icon_path, confidence=0.7)
    if image_coordinates is None:
        return image_coordinates

    image_center_coordinates = pyautogui.center(image_coordinates)
    if is_osx():
        x = image_center_coordinates[0] / 2
        y = image_center_coordinates[1] / 2
        image_center_coordinates = x, y

    pyautogui.moveTo(image_center_coordinates[0], image_center_coordinates[1], 1)
    pyautogui.click(image_center_coordinates[0], image_center_coordinates[1])
    return image_center_coordinates
