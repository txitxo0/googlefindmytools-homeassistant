#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import binascii
import requests
from bs4 import BeautifulSoup

from auth.aas_token_retrieval import get_aas_token
from auth.adm_token_retrieval import get_adm_token
from auth.username_provider import get_username


def nova_request(api_scope, hex_payload):
    url = "https://android.googleapis.com/nova/" + api_scope

    android_device_manager_oauth_token = get_adm_token(get_username())

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Authorization": "Bearer " + android_device_manager_oauth_token,
        "Accept-Language": "en-US",
        "User-Agent": "fmd/20006320; gzip"
    }

    payload = binascii.unhexlify(hex_payload)

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.content.hex()
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        print("[NovaRequest] Error: ", soup.get_text())


if __name__ == '__main__':
    print(get_aas_token())