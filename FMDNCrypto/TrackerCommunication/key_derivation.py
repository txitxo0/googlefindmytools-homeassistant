from FMDNCrypto.util import hexadecimal, hex_encoded_string, calculate_truncated_sha256
import hashlib
import hmac

class FMDNOwnerOperations:

    def __init__(self):
        self.recovery_key = None
        self.ringing_key = None
        self.tracking_key = None

    def generate_keys(self, ephemeral_identity_key_hex: str):

        try:
            self.recovery_key = calculate_truncated_sha256(ephemeral_identity_key_hex, 0x01)
            self.ringing_key = calculate_truncated_sha256(ephemeral_identity_key_hex, 0x02)
            self.tracking_key = calculate_truncated_sha256(ephemeral_identity_key_hex, 0x03)

            print(f"Generated Keys: {hex_encoded_string(self.recovery_key)} {hex_encoded_string(self.ringing_key)} {hex_encoded_string(self.tracking_key)}")
        except Exception as e:
            print(str(e))