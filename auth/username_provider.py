#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
from auth.token_cache import get_cached_value

username_string = 'username'

def get_username():

    username = get_cached_value(username_string)

    if username is not None:
        return username

    return ""

if __name__ == '__main__':
    get_username()