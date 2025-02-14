#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from FMDNCrypto.sha import calculate_truncated_sha256

class FMDNOwnerOperations:

    def __init__(self):
        self.recovery_key = None
        self.ringing_key = None
        self.tracking_key = None

    def generate_keys(self, identity_key: bytes):

        try:
            self.recovery_key = calculate_truncated_sha256(identity_key, 0x01)
            self.ringing_key = calculate_truncated_sha256(identity_key, 0x02)
            self.tracking_key = calculate_truncated_sha256(identity_key, 0x03)

        except Exception as e:
            print(str(e))