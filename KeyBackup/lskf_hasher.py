#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
from binascii import unhexlify

import pyscrypt
from example_data_provider import get_example_data


def ascii_to_bytes(string):
    return string.encode('ascii')


def get_lskf_hash(pin: str, salt: bytes) -> bytes:
    # Parameters
    data_to_hash = ascii_to_bytes(pin)  # Convert the string to an ASCII byte array

    log_n_cost = 4096  # CPU/memory cost parameter
    block_size = 8  # Block size
    parallelization = 1  # Parallelization factor
    key_length = 32  # Length of the derived key in bytes

    # Perform Scrypt hashing
    hashed = pyscrypt.hash(
        password=data_to_hash,
        salt=salt,
        N=log_n_cost,
        r=block_size,
        p=parallelization,
        dkLen=key_length
    )

    return hashed

if __name__ == '__main__':

    sample_pin = get_example_data("sample_pin")
    sample_pin_salt = unhexlify(get_example_data("sample_pin_salt"))

    print(get_lskf_hash(sample_pin, sample_pin_salt).hex())