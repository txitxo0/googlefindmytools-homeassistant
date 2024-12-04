#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import binascii

from NovaApi.util import generate_random_uuid
from ProtoDecoders import DeviceUpdate_pb2

def get_security_domain_request_url():
    encryption_unlock_request_extras = DeviceUpdate_pb2.EncryptionUnlockRequestExtras()
    encryption_unlock_request_extras.operation = 1
    encryption_unlock_request_extras.securityDomain.name = "finder_hw"
    encryption_unlock_request_extras.securityDomain.unknown = 0
    encryption_unlock_request_extras.sessionId = generate_random_uuid()

    # serialize and print as base64
    serialized = encryption_unlock_request_extras.SerializeToString()

    scope = "https://accounts.google.com/encryption/unlock/android?kdi="

    url = scope + binascii.b2a_base64(serialized).decode('utf-8')
    return url

if __name__ == '__main__':
    print(get_security_domain_request_url())