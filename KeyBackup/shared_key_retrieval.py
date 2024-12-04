#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from Auth.token_cache import get_cached_value_or_set
from KeyBackup.shared_key_flow import request_shared_key_flow


def _retrieve_shared_key():
    shared_key = request_shared_key_flow()

    return shared_key


def get_shared_key():
    return get_cached_value_or_set('shared_key', _retrieve_shared_key)


if __name__ == '__main__':
    print(get_shared_key())