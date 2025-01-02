#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import time
import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait

def request_oauth_account_token_flow():
    # Set up Chrome options
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.binary_location = r"INSERT_PATH_TO_CHROME_BINARY_HERE"

    print("""[AuthFlow] This script will now open Google Chrome on your device to login to your Google account.
> Please make sure that Chrome is installed on your system.
> For macOS users only: Make that you allow Python (or PyCharm) to control Chrome if prompted. 
    """)

    # Press enter to continue
    input("[AuthFlow] Press Enter to continue...")

    # Automatically install and set up the Chrome driver
    print("[AuthFlow] Installing ChromeDriver...")

    try:
        driver = uc.Chrome(options=chrome_options)
        print("[AuthFlow] ChromeDriver installed and browser started.")
    except Exception as e:
        raise Exception("[AuthFlow] Failed to install ChromeDriver. Chrome was not detected on your system.\n\nIf you know that Chrome is installed, open the file 'Auth/auth_flow.py' and set the path to your Chrome executable in line 16.")

    try:
        # Open the browser and navigate to the URL
        print("[AuthFlow] Navigating to the URL...")
        start_time = time.time()
        driver.get("https://accounts.google.com/EmbeddedSetup")
        print(f"[AuthFlow] Page loaded in {time.time() - start_time:.2f} seconds.")

        # Wait until the "oauth_token" cookie is set
        print("[AuthFlow] Waiting for 'oauth_token' cookie to be set...")
        WebDriverWait(driver, 300).until(
            lambda d: d.get_cookie("oauth_token") is not None
        )

        # Get the value of the "oauth_token" cookie
        oauth_token_cookie = driver.get_cookie("oauth_token")
        oauth_token_value = oauth_token_cookie['value']

        # Print the value of the "oauth_token" cookie
        print("oauth_token:", oauth_token_value)

        return oauth_token_value

    finally:
        # Close the browser
        print("[AuthFlow] Closing the browser...")
        driver.quit()

if __name__ == '__main__':
    request_oauth_account_token_flow()