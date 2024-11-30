import binascii
import requests
from bs4 import BeautifulSoup

from private import sample_android_device_manager_oauth_token

def nova_request(api_scope, hex_payload):
    url = "https://android.googleapis.com/nova/" + api_scope

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Authorization": "Bearer " + sample_android_device_manager_oauth_token, # Insert your OAuth token here
        "Accept-Language": "en-US",
        "User-Agent": "fmd/20006320; gzip"
    }

    payload = binascii.unhexlify(hex_payload)

    response = requests.post(url, headers=headers, data=payload)
    print("[NovaRequest] Status Code:", response.status_code)
    print("[NovaRequest] Response Hex: ", response.content.hex())

    if response.status_code == 200:
        print("[NovaRequest] Request performed successfully.")
        return response.content.hex()
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        print("[NovaRequest] Error: ", soup.get_text())