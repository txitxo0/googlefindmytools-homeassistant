from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from binascii import unhexlify
from TitanBackup.lskf_hasher import get_lskf_hash, ascii_to_bytes
from private import sample_pin, sample_pin_salt, sample_encrypted_recovery_key, sample_encrypted_application_key


def derive_key_using_hkdf_sha256(input_key: bytes, salt: bytes, info: bytes) -> bytes:
    hkdf = HKDF(
        algorithm=SHA256(),
        length=16,
        salt=salt,
        info=info,
        backend=default_backend(),
    )
    return hkdf.derive(input_key)


def decrypt_aes_gcm_with_derived_key(key: bytes, key_type_string: bytes, encrypted: bytes) -> bytes:
    VERSION = b"\x02\x00"

    if len(encrypted) < 2 or encrypted[:2] != VERSION:
        raise ValueError("Invalid version in encrypted data")

    offset = len(VERSION)

    iv = encrypted[offset : offset + 12]
    offset += 12
    ciphertext = encrypted[offset:]

    hkdf_salt = b"SECUREBOX" + VERSION
    hkdf_info = b"SHARED HKDF-SHA-256 AES-128-GCM"

    derived_key = derive_key_using_hkdf_sha256(key, hkdf_salt, hkdf_info)

    aes_gcm = AESGCM(derived_key)
    return aes_gcm.decrypt(iv, ciphertext, key_type_string)


def decrypt_recovery_key(lskf_hash, encrypted_recovery_key):
    return decrypt_aes_gcm_with_derived_key(lskf_hash, ascii_to_bytes("V1 locally_encrypted_recovery_key"), unhexlify(encrypted_recovery_key))


def decrypt_application_key(recovery_key, encrypted_application_key):
    return decrypt_aes_gcm_with_derived_key(recovery_key, ascii_to_bytes("V1 encrypted_application_key"), unhexlify(encrypted_application_key))


if __name__ == '__main__':

    pin = sample_pin
    pin_salt = sample_pin_salt
    encrypted_recovery_key = sample_encrypted_recovery_key
    encrypted_application_key = sample_encrypted_application_key

    lskf_hash = get_lskf_hash(pin, pin_salt)
    recovery_key = decrypt_recovery_key(lskf_hash, encrypted_recovery_key)
    application_key = decrypt_application_key(recovery_key, encrypted_application_key)

    print("Application Key was found:")
    print(application_key.hex())