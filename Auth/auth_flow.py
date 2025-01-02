#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import time
import subprocess
from playwright.sync_api import sync_playwright

def request_oauth_account_token_flow():
    print("""[AuthFlow] This script will now open a browser to log in to your Google account.
> Please make sure that you are ready to log in.
> For macOS users only: Ensure that you allow Python (or your terminal) to control the browser if prompted.
    """)

    # Press enter to continue
    input("[AuthFlow] Press Enter to continue...")

    # Ensure Playwright browsers are installed
    print("[AuthFlow] Ensuring Playwright browsers are installed...")
    try:
        subprocess.run(["playwright", "install"], check=True)
    except subprocess.CalledProcessError as e:
        raise Exception("[AuthFlow] Failed to install Playwright browsers. Ensure Playwright is properly installed.") from e

    print("[AuthFlow] Launching browser...")

    with sync_playwright() as p:
        # Launch Chromium in non-headless mode
        browser = p.chromium.launch(headless=False, args=['--disable-blink-features=AutomationControlled'])
        context = browser.new_context()
        page = context.new_page()

        try:
            # Open the browser and navigate to the URL
            print("[AuthFlow] Navigating to the URL...")
            start_time = time.time()
            page.goto("https://accounts.google.com/EmbeddedSetup", timeout=60000)
            print(f"[AuthFlow] Page loaded in {time.time() - start_time:.2f} seconds.")

            # Wait for the "oauth_token" cookie to be set (polling every 1 second)
            print("[AuthFlow] Waiting for 'oauth_token' cookie to be set...")
            timeout = 300  # 5 minutes timeout
            start_time = time.time()
            oauth_token_cookie = None
            while time.time() - start_time < timeout:
                cookies = context.cookies()
                oauth_token_cookie = next(
                    (cookie for cookie in cookies if cookie["name"] == "oauth_token"), None
                )
                if oauth_token_cookie:
                    break
                time.sleep(1)  # Wait 1 second before checking again

            if not oauth_token_cookie:
                raise Exception("[AuthFlow] 'oauth_token' cookie was not set within the timeout period.")

            oauth_token_value = oauth_token_cookie['value']

            # Print the value of the "oauth_token" cookie
            print("oauth_token:", oauth_token_value)

            return oauth_token_value

        finally:
            # Close the browser
            print("[AuthFlow] Closing the browser...")
            browser.close()

if __name__ == '__main__':
    request_oauth_account_token_flow()