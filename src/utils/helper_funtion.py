"""
helper funtions
"""

import os
import sys
import time
import shutil
import base64
import tkinter as tk
import pyautogui
from openai import OpenAI
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from src.components.pyautogui.detect_icon import detect_icon_with_retry
from src.components.pdfminer.extract_pdf_text import extract_pdf_text

load_dotenv()
model = OpenAI()
model.timeout = 10
screenshot_path = "screenshot.jpg"


chrome_options = uc.ChromeOptions()

def get_chrome_profile_path():
    if sys.platform.startswith("win"):
        base_path = os.path.join(os.getenv("LOCALAPPDATA"), "Google", "Chrome", "User Data")
    elif sys.platform.startswith("darwin"):
        base_path = os.path.expanduser("~/Library/Application Support/Google/Chrome")
    elif sys.platform.startswith("linux"):
        base_path = os.path.expanduser("~/.config/google-chrome")
    else:
        return None
    
    default_profile = os.path.join(base_path, "Default")    
    # Check if the path exists
    if os.path.exists(default_profile):
        return default_profile
    else:
        # If "Default" does not exist, check if another profile (e.g., "Profile 1") exists
        other_profiles = [p for p in os.listdir(base_path) if p.startswith("Profile")]
        if other_profiles:
            return os.path.join(base_path, other_profiles[0])
    return None

def show_custom_message(title, text, duration = 3):
    def countdown(count):
        label.config(text=f"{text}\nClosing in {count} seconds...")
        if count > 0:
            custom_box.after(1000, countdown, count - 1)
        else:
            custom_box.destroy()

    custom_box = tk.Tk()
    custom_box.title(title)
    custom_box.geometry('300x150')
    custom_box.configure(bg='orange')  # Border color
    frame = tk.Frame(custom_box, bg='white', padx=10, pady=10)
    frame.pack(padx=5, pady=5, expand=True, fill='both')
    label = tk.Label(frame, text=text, bg='white', font=('Arial', 12))
    label.pack(pady=10)
    countdown(duration)
    custom_box.mainloop()

def move_pdf_to_finance_assets():
    source_dir = "./data"
    destination_dir = "./src/financial_crew/assets"
    files = os.listdir(source_dir)
    for file_name in files:
        source_file = os.path.join(source_dir, file_name)
        destination_file = os.path.join(destination_dir, file_name)
        shutil.copy(source_file, destination_file)
        print(f"Copied {file_name} to {destination_dir}")

async def process_icon(image_path, operation_delay):
    cords = detect_icon_with_retry(image_path, attempts=3, delay=operation_delay)
    if cords is not None:
        return cords
    else:
        return cords


def error_message(message, browser, display):
    browser.quit()
    display.stop()
    return message


def image_b64(image):
    with open(image, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_email_attachment_summary(pdf_content):
    response = model.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Your job is to answer the user's question based on the given screenshot of a website. Answer the user as an assistant, but don't tell that the information is from a screenshot or an image.",
            },
            {
                "role": "user",
                "content": f"""As a helpful assistant, read the below context carefully and give me the main points of the context in bullet points. Remember that do not include any information which is not relevant to the context.
                CONTEXT: {pdf_content}""",
            },
        ],
        max_tokens=1024,
    )
    print(response)
    email_attatchment_response = response.choices[0].message
    email_attatchment_response = email_attatchment_response.content
    return email_attatchment_response


def get_email_body_summary(screenshot_path):
    base64_image = image_b64(screenshot_path)
    response = model.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "Your job is to answer the user's question based on the given screenshot of a website. Answer the user as an assistant, but don't tell that the information is from a screenshot or an image.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                    {
                        "type": "text",
                        "text": "Here's the screenshot of the email. Just give me the main points of the email in bullet points.",
                    },
                ],
            },
        ],
        max_tokens=1024,
    )
    time.sleep(3)
    message = response.choices[0].message
    email_body_response = message.content
    # Delete the screenshot file
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)
    return email_body_response


def check_unread_email(browser):
    # Find all unread emails
    unread_emails = browser.find_elements(By.CSS_SELECTOR, "tr.zA.zE")
    if len(unread_emails) > 1:
        return unread_emails
    else:
        print("No second unread email found")
        return unread_emails


def download_email_attachment(browser, link):
    browser.execute_cdp_cmd(
        "Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": "./data"}
    )
    try:
        browser.get(link)
        print(f"Navigated to download link: {link}")
    except Exception as error:
        print(f"Failed to Download File: {error}")


def process_unread_emails(browser, unread_emails):
    final_response = ""
    global screenshot_path  # pylint: disable=global-variable-not-assigned
    for email in unread_emails:
        email.click()  # Open the email
        time.sleep(3)  # Wait for the email to load

        # Take a screenshot after the action
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        email_bullet_points = get_email_body_summary(screenshot_path)
        attachment_email_response = "No Attachment"
        try:
            attachment_element = browser.find_element(By.CSS_SELECTOR, "a.aQy.aZr.e")
            if attachment_element:
                attachment_url = attachment_element.get_attribute("href")
                attachment_url = attachment_url.replace("disp=inline", "disp=safe")
                download_email_attachment(browser, attachment_url)
                time.sleep(3)
                pdf_content = extract_pdf_text()
                time.sleep(2)
                attachment_email_response = get_email_attachment_summary(pdf_content)
                time.sleep(5)
            else:
                print("No attachment found")
        except:
            print("No attachment element found")

        # Format the email response
        email_response = f"""
**# Email #**

Email Body Summary:
{email_bullet_points}

Attachment Summary:
{attachment_email_response}
"""
        final_response += email_response
        move_pdf_to_finance_assets()
        # Delete downloaded file
        folder_path = "./data"
        files = os.listdir(folder_path)
        for file in files:
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)
        # Navigate back to the unread email list
        browser.back()
        time.sleep(2)  # Wait for the list to reload
    return final_response
