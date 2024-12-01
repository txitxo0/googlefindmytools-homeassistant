#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from binascii import unhexlify
import pyscrypt
from private import sample_pin, sample_pin_salt


def ascii_to_bytes(string):
    return string.encode('ascii')


def get_lskf_hash(pin, salt):
    # Parameters
    data_to_hash = ascii_to_bytes(pin)  # Convert the string to an ASCII byte array

    log_n_cost = 4096  # CPU/memory cost parameter
    block_size = 8  # Block size
    parallelization = 1  # Parallelization factor
    key_length = 32  # Length of the derived key in bytes

    # Perform Scrypt hashing
    hashed = pyscrypt.hash(
        password=data_to_hash,
        salt=unhexlify(salt),
        N=log_n_cost,
        r=block_size,
        p=parallelization,
        dkLen=key_length
    )

    return hashed

if __name__ == '__main__':
   print(get_lskf_hash(sample_pin, sample_pin_salt).hex())