#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from auth.token_retrieval import request_token
from auth.username_provider import get_username

def get_spot_token(username):
    return request_token(username, "spot", True)

if __name__ == '__main__':
    print(get_spot_token(get_username()))