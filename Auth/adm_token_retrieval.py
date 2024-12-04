#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from Auth.token_retrieval import request_token
from Auth.username_provider import get_username

cached_adm_token = None

def get_adm_token(username):

    global cached_adm_token

    if cached_adm_token:
        print("[AdmTokenRetrieval] Using Cached App Token.")
        return cached_adm_token

    cached_adm_token = request_token(username, "android_device_manager")
    return cached_adm_token


if __name__ == '__main__':
    print(get_adm_token(get_username()))