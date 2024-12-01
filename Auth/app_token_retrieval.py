#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import gpsoauth

from Auth.aas_token_retrieval import get_aas_token
from Auth.android_id_generator import get_android_id
from Auth.username_provider import get_username

cached_adm_token = None

def _generate_adm_token(username):

    print("[AppTokenRetrieval] Asking Server for App Token.")

    aas_token = get_aas_token()
    android_id = get_android_id()

    auth_response = gpsoauth.perform_oauth(
        username, aas_token, android_id,
        service='oauth2:https://www.googleapis.com/auth/android_device_manager',
        app='com.google.android.apps.adm',
        client_sig='38918a453d07199354f8b19af05ec6562ced5788')
    token = auth_response['Auth']

    return token


def get_adm_token(username):

    global cached_adm_token

    if cached_adm_token:
        print("[AppTokenRetrieval] Using Cached App Token.")
        return cached_adm_token

    cached_adm_token = _generate_adm_token(username)
    return cached_adm_token


if __name__ == '__main__':
    get_adm_token(get_username())