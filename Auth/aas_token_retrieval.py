#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import gpsoauth

from Auth.android_id_generator import get_android_id
from Auth.token_cache import get_cached_value
from Auth.username_provider import get_username
from private import sample_oauth_account_token


def _generate_aas_token():
    username = get_username()
    android_id = get_android_id()
    token = sample_oauth_account_token

    print("[AASTokenRetrieval] Asking Server for AAS Token.")
    aas_token_response = gpsoauth.exchange_token(username, token, android_id)
    aas_token = aas_token_response['Token']

    return aas_token


def get_aas_token():
    return get_cached_value('aas_token', _generate_aas_token)


if __name__ == '__main__':
    print(get_aas_token())