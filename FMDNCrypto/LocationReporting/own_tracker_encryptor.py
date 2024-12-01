#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import secrets

from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from binascii import unhexlify, hexlify

from private import sample_identity_key, sample_location_data

def to_hex(byte_array):
    return hexlify(byte_array).decode()

def encrypt_with_hashed_key(data, identity_key, iv):
    assert len(iv) == 12, "Invalid IV"
    assert len(identity_key) == 32, "Invalid identity key"
    return encrypt_bytes(get_message_digest(identity_key), data, iv)

def encrypt_bytes(key, data, iv):
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return iv + ciphertext + tag

def get_message_digest(byte_string):
    hasher = SHA256.new()
    hasher.update(byte_string)
    hashed_key = hasher.digest()
    print("Hashed key: " + to_hex(hashed_key))
    return hashed_key

def decrypt_bytes(key, encrypted_data):
    hashed_key = get_message_digest(key)
    iv = encrypted_data[:12]
    ciphertext = encrypted_data[12:-16]
    tag = encrypted_data[-16:]
    cipher = AES.new(hashed_key, AES.MODE_GCM, nonce=iv)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data

if __name__ == "__main__":
    # EIK (32 bytes)
    key = unhexlify(sample_identity_key)

    # Protobuf location data
    data = unhexlify(sample_location_data)

    # IV is 12 bytes
    iv = secrets.token_bytes(12)

    encrypted = encrypt_with_hashed_key(data, key, iv)
    print("EncryptedAndHashed: " + to_hex(encrypted))

    decrypted = decrypt_bytes(key, encrypted)
    print("Decrypted: " + to_hex(decrypted))

    assert to_hex(data) == to_hex(decrypted), "Decryption failed"