#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from uuid import getnode as getmac

from Auth.token_cache import get_cached_value


def _create_mac_string(num, splitter=':'):
    mac = f"{num:012X}"
    mac = splitter.join(mac[i:i + 2] for i in range(0, 12, 2))
    return mac


def _generate_android_id():
    print("[AndroidIdGenerator] Generating new AndroidID.")
    mac_int = getmac()
    if (mac_int >> 40) % 2:
        raise OSError("MAC is invalid")

    android_id = _create_mac_string(mac_int).replace(':', '')
    return android_id


def get_android_id():
    return get_cached_value('android_id', _generate_android_id)


if __name__ == '__main__':
    print(get_android_id())