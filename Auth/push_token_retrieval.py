#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from Auth.app_token_retrieval import request_fmdn_app_token
from Auth.username_provider import get_username

cached_push_token = None

def get_push_token(username):

    global cached_push_token

    if cached_push_token:
        print("[AppTokenRetrieval] Using Cached Push Token.")
        return cached_push_token

    cached_push_token = request_fmdn_app_token(username, "notifications")
    return cached_push_token


if __name__ == '__main__':
    print(get_push_token(get_username()))