#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
import os
from NovaApi.ListDevices.nbe_list_devices import list_devices
from auth.fcm_receiver import FcmReceiver

def check_and_run_auth_flow():
    secrets_path = os.path.join('auth', 'secrets.json')
    if not os.path.exists(secrets_path):
        print("auth/secrets.json not found. Running authentication flow...")
        try:
            from chrome_driver import create_and_get_driver
            from auth.auth_flow import auth_flow
            driver = create_and_get_driver()
            auth_flow(driver)
            driver.quit()
            print("Authentication flow completed successfully.")
        except ImportError:
            print("Could not import authentication modules. Please ensure you have the dev dependencies installed.")
        except Exception as e:
            print(f"An error occurred during the authentication flow: {e}")

if __name__ == '__main__':
    check_and_run_auth_flow()
    fcm_receiver = FcmReceiver()
    try:
        list_devices(fcm_receiver)
    finally:
        # Ensure the FCM receiver connection is closed
        fcm_receiver.stop_listening()
