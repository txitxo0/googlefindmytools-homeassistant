#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
import struct

class GrpcParser:
    @staticmethod
    def extract_grpc_payload(grpc: bytes) -> bytes:
        if len(grpc) < 5:
            raise ValueError("Invalid GRPC payload")

        # Extract the length bytes and interpret them as a big-endian unsigned 32-bit integer
        grpc_len_data = grpc[1:5]
        uint_value = struct.unpack(">I", grpc_len_data)[0]
        length = int(uint_value)

        if len(grpc) < 5 + length:
            raise ValueError("Invalid GRPC payload length")

        # Extract the payload
        data = grpc[5:5 + length]

        return data

    @staticmethod
    def construct_grpc(payload: bytes) -> bytes:
        # not compressed
        compressed = bytes([0])

        length = len(payload)
        length_data = struct.pack(">I", length)

        return compressed + length_data + payload