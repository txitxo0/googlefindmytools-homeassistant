#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
from ProtoDecoders import Common_pb2
from ProtoDecoders import DeviceUpdate_pb2
from SpotApi.spot_request import spot_request

def get_eid_info():
    getEidInfoForE2eeDevicesRequest = Common_pb2.GetEidInfoForE2eeDevicesRequest()
    getEidInfoForE2eeDevicesRequest.ownerKeyVersion = -1
    getEidInfoForE2eeDevicesRequest.hasOwnerKeyVersion = True

    serialized_request = getEidInfoForE2eeDevicesRequest.SerializeToString()
    response_bytes = spot_request("GetEidInfoForE2eeDevices", serialized_request)

    eid_info = DeviceUpdate_pb2.GetEidInfoForE2eeDevicesResponse()
    eid_info.ParseFromString(response_bytes)

    return eid_info


if __name__ == '__main__':
    print(get_eid_info().encryptedOwnerKeyAndMetadata.encryptedOwnerKey.hex())