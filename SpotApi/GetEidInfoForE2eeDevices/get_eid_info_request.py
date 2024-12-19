#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
import struct
from binascii import unhexlify

from ProtoDecoders import DeviceUpdate_pb2
from SpotApi.spot_request import spot_request

def get_eid_info():
    # TODO fix this, use proper Protobuf class
    hex_result = spot_request("GetEidInfoForE2eeDevices", "000000000D08FFFFFFFFFFFFFFFFFF011001")

    response_bytes = bytes.fromhex(hex_result)
    grpc_payload = extract_grpc_payload(response_bytes)

    eid_info = DeviceUpdate_pb2.GetEidInfoForE2eeDevicesResponse()
    eid_info.ParseFromString(grpc_payload)

    return eid_info


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


if __name__ == '__main__':
    print(get_eid_info().encryptedOwnerKeyAndMetadata.encryptedOwnerKey.hex())