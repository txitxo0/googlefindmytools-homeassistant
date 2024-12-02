#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

# Decrypts the advertised beacon state from the Bluetooth advertisement of the tracker

from binascii import unhexlify, hexlify
from Cryptodome.Cipher import AES

from example_data_provider import get_example_data


def get_beacon_parameters(account_key, ciphertext_hex):

    # Convert hex to bytes
    ciphertext = unhexlify(ciphertext_hex)
    key_bytes = unhexlify(account_key)

    # Create AES cipher in ECB mode
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    # Decrypt the ciphertext
    plaintext = cipher.decrypt(ciphertext)

    # Convert plaintext to hex
    plaintext_hex = hexlify(plaintext).decode()

    # Print the decrypted plaintext as hex
    return plaintext_hex

if __name__ == '__main__':
    sample_identity_key = get_example_data("sample_identity_key")

    print("Decrypted Beacon State (hex): " + get_beacon_parameters(sample_identity_key, "4773d81b1ff6059ca956ba10695ce414"))