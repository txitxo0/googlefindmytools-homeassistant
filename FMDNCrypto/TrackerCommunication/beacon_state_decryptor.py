#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

# Decrypts the advertised beacon state from the Bluetooth advertisement of the tracker

from binascii import unhexlify, hexlify
from Cryptodome.Cipher import AES

from private import sample_account_key

def get_beacon_parameters():
    # Hex-encoded ciphertext and key
    ciphertext_hex = "4773d81b1ff6059ca956ba10695ce414" # Example ciphertext
    key_hex = sample_account_key

    # Convert hex to bytes
    ciphertext = unhexlify(ciphertext_hex)
    key = unhexlify(key_hex)

    # Create AES cipher in ECB mode
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt the ciphertext
    plaintext = cipher.decrypt(ciphertext)

    # Convert plaintext to hex
    plaintext_hex = hexlify(plaintext).decode()

    # Print the decrypted plaintext as hex
    return plaintext_hex

if __name__ == '__main__':
    print("Decrypted Beacon State (hex): " + get_beacon_parameters())