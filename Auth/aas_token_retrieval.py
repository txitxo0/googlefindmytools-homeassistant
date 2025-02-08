#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import gpsoauth

from Auth.auth_flow import request_oauth_account_token_flow
from Auth.fcm_receiver import FcmReceiver
from Auth.token_cache import get_cached_value_or_set
from Auth.username_provider import get_username


def _generate_aas_token():
    username = get_username()
    android_id = FcmReceiver().get_android_id()
    token = request_oauth_account_token_flow()

    aas_token_response = gpsoauth.exchange_token(username, token, android_id)
    aas_token = aas_token_response['Token']

    return aas_token


def get_aas_token():
    return get_cached_value_or_set('aas_token', _generate_aas_token)


if __name__ == '__main__':
    print(get_aas_token())