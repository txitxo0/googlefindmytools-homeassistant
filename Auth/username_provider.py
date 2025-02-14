#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from Auth.token_cache import get_cached_value_or_set

def get_username():
    return get_cached_value_or_set('username', lambda: input("[UsernameProvider] Username was not setup yet. Type your Google Username/Email and press 'Enter':"))

if __name__ == '__main__':
    get_username()