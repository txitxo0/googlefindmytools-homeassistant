#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
import secrets

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from binascii import unhexlify
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

from KeyBackup.lskf_hasher import ascii_to_bytes, get_lskf_hash


# Constants
VERSION = b'\x02\x00'
SECUREBOX = b'SECUREBOX'
SHARED_HKDF_AES_GCM = b'SHARED HKDF-SHA-256 AES-128-GCM'
P256_HKDF_AES_GCM = b'P256 HKDF-SHA-256 AES-128-GCM'


def derive_key_using_hkdf_sha256(input_key: bytes, salt: bytes, info: bytes) -> bytes:

    # Create 16-byte HKDF instance
    hkdf = HKDF(
        algorithm=SHA256(),
        length=16,
        salt=salt,
        info=info,
        backend=default_backend(),
    )

    # Derive key using HKDF
    return hkdf.derive(input_key)


def decrypt_aes_gcm_with_derived_key(encrypted_data: bytes, private_key: bytes, key_type_string: bytes,
                                     derive_with_public_key=False) -> bytes:

    # Only supporting specified version, else return
    if len(encrypted_data) < 2 or encrypted_data[:2] != VERSION:
        raise ValueError("Invalid version or data length")

    version_length = len(VERSION)

    # Get ciphertext and iv from encrypted key data
    ciphertext_offset = 65 if derive_with_public_key else 0
    ciphertext_and_iv = encrypted_data[version_length + ciphertext_offset:]

    # Create HKDF salt and info
    hkdf_salt = SECUREBOX + VERSION
    hkdf_info = P256_HKDF_AES_GCM if derive_with_public_key else SHARED_HKDF_AES_GCM

    if derive_with_public_key:
        # Perform key exchange and derive shared secret
        shared_public_key = encrypted_data[version_length:version_length + ciphertext_offset]
        private_key = derive_shared_secret(private_key, shared_public_key)

    # Derive key using HKDF
    derived_key = derive_key_using_hkdf_sha256(private_key, hkdf_salt, hkdf_info)

    # Decrypt data with AES-GCM
    return decrypt_aes_gcm(derived_key, ciphertext_and_iv, key_type_string)


def derive_shared_secret(private_key_jwt: bytes, public_key: bytes) -> bytes:

    # Extract EC private curve from JWT format
    private_key_bytes = private_key_jwt[:32]
    private_key = ec.derive_private_key(int.from_bytes(private_key_bytes, "big"), ec.SECP256R1(), default_backend())

    # Create public key from bytes
    public_key = ec.EllipticCurvePublicKey.from_encoded_point(ec.SECP256R1(), public_key)

    # Perform ECDH key exchange to calculate shared secret
    return private_key.exchange(ec.ECDH(), public_key)


def decrypt_aes_gcm(key: bytes, encrypted_data_and_iv: bytes, additional_data: bytes = None, iv_length = 12) -> bytes:

    # IV is prepended to encrypted data
    iv = encrypted_data_and_iv[:iv_length]
    ciphertext = encrypted_data_and_iv[iv_length:]

    # Perform AES-GCM
    aes_gcm = AESGCM(key)
    decrypted_data = aes_gcm.decrypt(iv, ciphertext, additional_data)

    # Return result
    return decrypted_data


def encrypt_aes_gcm(key: bytes, plaintext: bytes, additional_data=None, iv_length=12) -> bytes:
    # Generate a random IV
    iv = secrets.token_bytes(iv_length)

    # Perform AES-GCM
    aes_gcm = AESGCM(key)
    ciphertext = aes_gcm.encrypt(iv, plaintext, additional_data)

    # Prepend IV to the ciphertext
    return iv + ciphertext


def decrypt_aes_cbc_no_padding(key: bytes, encrypted_data_and_iv: bytes, iv_length = 16) -> bytes:

    # IV is prepended to encrypted data
    iv = encrypted_data_and_iv[:iv_length]
    ciphertext = encrypted_data_and_iv[iv_length:]

    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )

    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    return decrypted_data


def decrypt_recovery_key(lskf_hash: bytes, encrypted_recovery_key: bytes) -> bytes:

    # The recovery key is encrypted using the hash of the LSKF
    return decrypt_aes_gcm_with_derived_key(encrypted_recovery_key, lskf_hash,
                                            ascii_to_bytes("V1 locally_encrypted_recovery_key"))


def decrypt_application_key(recovery_key: bytes, encrypted_application_key: bytes) -> bytes:

    # The application key is encrypted using the recovery key
    return decrypt_aes_gcm_with_derived_key(encrypted_application_key, recovery_key,
                                            ascii_to_bytes("V1 encrypted_application_key"))


def decrypt_security_domain_key(application_key: bytes, encrypted_security_domain_key: bytes) -> bytes:

    # The security domain key is encrypted using the application key
    return decrypt_aes_gcm(application_key, encrypted_security_domain_key)


def decrypt_shared_key(security_domain_key: bytes, encrypted_shared_key: bytes) -> bytes:

    # The shared key is encrypted using the security domain key
    return decrypt_aes_gcm_with_derived_key(encrypted_shared_key, security_domain_key,
                                            ascii_to_bytes("V1 shared_key"), True)


def decrypt_owner_key(shared_key: bytes, encrypted_owner_key: bytes) -> bytes:

    # The owner key is encrypted using the shared key. The owner key is valid for all trackers
    return decrypt_aes_gcm(shared_key, encrypted_owner_key)


def decrypt_eik(owner_key: bytes, encrypted_eik: bytes) -> bytes:

    # The EIK is encrypted using the owner key. The EIK is only valid for a certain tracker
    if len(encrypted_eik) == 48:
        return decrypt_aes_cbc_no_padding(owner_key, encrypted_eik)

    if len(encrypted_eik) == 60:
        return decrypt_aes_gcm(owner_key, encrypted_eik)

    raise ValueError("The encrypted EIK has invalid length!")


def decrypt_account_key(owner_key: bytes, encrypted_account_key: bytes) -> bytes:

    # The account key is encrypted using the owner key. The account key is only valid for a certain tracker
    if len(encrypted_account_key) == 32:
        return decrypt_aes_cbc_no_padding(owner_key, encrypted_account_key)

    if len(encrypted_account_key) == 44:
        return decrypt_aes_gcm(owner_key, encrypted_account_key)

    raise ValueError("The encrypted Account Key has invalid length!")




