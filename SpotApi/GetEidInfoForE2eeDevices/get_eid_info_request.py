#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
from binascii import unhexlify

from ProtoDecoders import DeviceUpdate_pb2
from SpotApi.spot_request import spot_request

def get_eid_info():
    # TODO fix this, use proper Protobuf class
    hex_result = spot_request("GetEidInfoForE2eeDevices", "000000000D08FFFFFFFFFFFFFFFFFF011001")

    # remove the first 5 bytes and last 4 bytes (gRPC metadata)
    # TODO fix this, use proper gRPC library, might not work with all responses
    hex_result = hex_result[10:-8]

    eid_info = DeviceUpdate_pb2.GetEidInfoForE2eeDevicesResponse()
    eid_info.ParseFromString(bytes.fromhex(hex_result))

    return eid_info


if __name__ == '__main__':
    print(get_eid_info().encryptedOwnerKeyAndMetadata.encryptedOwnerKey.hex())