#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import hashlib
import hmac

def calculate_truncated_sha256(identity_key: bytes, operation: int) -> bytes:
    identity_key_bytes = identity_key
    data = identity_key_bytes + bytes([operation])

    sha256_hash = hashlib.sha256(data).digest()
    truncated_hash = sha256_hash[:8]

    return truncated_hash


def calculate_hmac_sha256(key, message):
    hmac_obj = hmac.new(key, message, hashlib.sha256)
    return hmac_obj.hexdigest()