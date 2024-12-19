#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc

from KeyBackup.response_parser import get_fmdn_shared_key
from KeyBackup.shared_key_request import get_security_domain_request_url

# Initialize undetected Chrome WebDriver
def create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    return uc.Chrome(options=options)

def request_shared_key_flow():
    driver = create_driver()
    try:
        # Step 1: Open Google accounts sign-in page
        driver.get("https://accounts.google.com/")

        # Step 2: Wait for user to sign in and redirect to https://myaccount.google.com
        WebDriverWait(driver, 300).until(
            EC.url_contains("https://myaccount.google.com")
        )
        print("User signed in successfully.")

        # Step 3: Open the security domain request URL
        security_url = get_security_domain_request_url()
        driver.get(security_url)

        # Step 4: Inject JavaScript interface
        script = """
        window.mm = {
            setVaultSharedKeys: function(str, vaultKeys) {
                console.log('setVaultSharedKeys called with:', str, vaultKeys);
                alert(JSON.stringify({ method: 'setVaultSharedKeys', str: str, vaultKeys: vaultKeys }));
            },
            closeView: function() {
                console.log('closeView called');
                alert(JSON.stringify({ method: 'closeView' }));
            }
        };
        """
        driver.execute_script(script)

        # Step 5: Listen for interactions
        print("JavaScript interface 'mm' is set. Waiting for interactions...")

        while True:
            # Check for alerts indicating JavaScript calls
            try:
                WebDriverWait(driver, 0.5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                message = alert.text
                alert.accept()

                print("Alert received:", message)
                print(message)

                # Parse the alert message
                import json
                data = json.loads(message)

                if data['method'] == 'setVaultSharedKeys':
                    print("setVaultSharedKeys called. Parsing vault keys...")
                    shared_key = get_fmdn_shared_key(data['vaultKeys'])
                    driver.quit()
                    return shared_key.hex()
                elif data['method'] == 'closeView':
                    print("closeView called. Closing browser.")
                    driver.quit()
                    break

            except Exception:
                pass

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
   request_shared_key_flow()
