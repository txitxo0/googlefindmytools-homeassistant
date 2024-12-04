#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import binascii
import httpx
import h2 # required for httpx to support HTTP/2
from bs4 import BeautifulSoup

from Auth.spot_token_retrieval import get_spot_token
from Auth.username_provider import get_username


def spot_request(api_scope, hex_payload):
    url = "https://spot-pa.googleapis.com/google.internal.spot.v1.SpotService/" + api_scope
    spot_oauth_token = get_spot_token(get_username())

    headers = {
        "User-Agent": "com.google.android.gms/244433022 grpc-java-cronet/1.69.0-SNAPSHOT",
        "Content-Type": "application/grpc",
        "Te": "trailers",
        "Authorization": "Bearer " + spot_oauth_token,
        "Grpc-Accept-Encoding": "gzip"
    }

    payload = binascii.unhexlify(hex_payload)

    # httpx is necessary because requests does not support the Te header
    with httpx.Client(http2=True) as client:
        response = client.post(url, headers=headers, content=payload)

        print("[SpotRequest] Status Code:", response.status_code)
        print("[SpotRequest] Response Hex: ", response.content.hex())

        if response.status_code == 200:
            print("[SpotRequest] Request performed successfully.")
            return response.content.hex()
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            print("[NovaRequest] Error: ", soup.get_text())

    return None