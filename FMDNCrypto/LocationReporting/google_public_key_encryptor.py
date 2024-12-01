#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import secrets
from binascii import unhexlify

from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import os

from private import sample_pk_secret_key, sample_pk_prefix, sample_pk_encoded_point, sample_pk_encoded_point_hmac

def hmac_sha256_hex(payload_hex, key_length):
    payload = unhexlify(payload_hex)

    # Step 1: Derive key using HKDF with SHA-256
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=key_length,
        salt=None,
        info=b'',
    )

    # Generate the key using the shared secret
    derived_key = hkdf.derive(payload)

    # Convert the result to a hex string
    return derived_key.hex()


class ECPublicKeyWrapper:
    def __init__(self, public_key):
        self.public_key = public_key


class CryptoParameters:
    def key_length(self):
        return 32  # Assuming 256-bit key

    def create_security_operation_from_key_material(self, key_material):
        # Stub for security operation creation; replace with your implementation
        return SecurityOperation1And2(key_material)


class SecurityOperation1And2:
    def __init__(self, key_material):
        self.sec_op1 = None  # Replace with actual security operation if needed
        self.sec_op2 = self.create_sec_op2(key_material)

    def create_sec_op2(self, key_material):
        # Stub for creating sec_op2
        return SecurityOperation(key_material)


class SecurityOperation:
    def __init__(self, key_material):
        self.key_material = key_material

    def encrypt(self, data, associated_data):
        # Example encryption using AES-GCM
        iv = secrets.token_bytes(12)  # 12 bytes for GCM
        cipher = Cipher(algorithms.AES(self.key_material), modes.GCM(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        encryptor.authenticate_additional_data(associated_data)
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return iv + ciphertext + encryptor.tag


class Encryptor:
    def __init__(self):
        self.publicKey = ECPublicKeyWrapper(self.generate_ec_public_key())
        self.cryptoParameters = CryptoParameters()

    def generate_ec_public_key(self):
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        return private_key.public_key()

    def encrypt(self, data, empty_data):
        eCPublicKey = self.publicKey.public_key
        key_length = self.cryptoParameters.key_length()

        # Create a new key pair
        private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
        eCPublicKey2 = private_key.public_key()

        # Generate shared secret
        shared_secret = private_key.exchange(ec.ECDH(), eCPublicKey)

        # Calculate HKDF
        hkdf_key = unhexlify(hmac_sha256_hex(shared_secret.hex(), 16))

        # Use the first 16 bytes of hkdfSha256
        mac2 = hkdf_key

        # Create security operation from key material
        create_security_operation_from_key_material = self.cryptoParameters.create_security_operation_from_key_material(
            mac2)
        security_operation = create_security_operation_from_key_material.sec_op1

        # Assume associated data (e.g., empty here)
        associated_data = bytearray()

        # Perform encryption
        if security_operation is not None:
            encrypted_data = security_operation.encrypt(data, associated_data)
        else:
            encrypted_data = create_security_operation_from_key_material.sec_op2.encrypt(data, associated_data)

        # Combine results
        byte_array = eCPublicKey2.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint
        )

        result = byte_array + encrypted_data

        return result


def encrypt(secret_key, prefix, encodedPoint, plaintext):
    # Ensure the secret key is the correct size (for AES, it should be 16, 24, or 32 bytes)
    assert len(secret_key) in {16, 24, 32}

    # Generate a random IV (12 bytes for GCM)
    iv = secrets.token_bytes(12) #0d8af4db1d15cfeb090518cf01

    assert len(iv) in {12}

    # Create AES GCM cipher
    cipher = Cipher(algorithms.AES(secret_key), modes.GCM(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Perform encryption
    ciphertext = encryptor.update(plaintext) + encryptor.finalize() + encryptor.tag

    print(ciphertext.hex())

    # Concatenate prefix, IV, and ciphertext
    return prefix + encodedPoint + iv + ciphertext


# Example usage
if __name__ == "__main__":
    encryptedData = (
        encrypt(unhexlify(sample_pk_secret_key), unhexlify(sample_pk_prefix), unhexlify(sample_pk_encoded_point), unhexlify(sample_pk_encoded_point_hmac)))

    print("Encoded Point HMAC: " + hmac_sha256_hex(sample_pk_encoded_point_hmac,16))
    print(encryptedData.hex())