#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import binascii

from NovaApi.util import generate_random_uuid
from ProtoDecoders import DeviceUpdate_pb2

# Generate a random, but fixed client ID for request identification for this session
client_id = generate_random_uuid()

def create_action_request(canonic_device_id, gcm_registration_id, request_uuid = generate_random_uuid(), fmd_client_uuid = client_id):
    actionRequest = DeviceUpdate_pb2.ExecuteActionRequest()

    actionRequest.scope.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    actionRequest.scope.device.canonicId.id = canonic_device_id

    actionRequest.requestMetadata.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    actionRequest.requestMetadata.requestUuid = request_uuid
    actionRequest.requestMetadata.fmdClientUuid = fmd_client_uuid
    actionRequest.requestMetadata.gcmRegistrationId.id = gcm_registration_id
    actionRequest.requestMetadata.unknown = True

    return actionRequest


def serialize_action_request(actionRequest):
    # Serialize to binary string
    binary_payload = actionRequest.SerializeToString()

    # Convert to hex string
    hex_payload = binascii.hexlify(binary_payload).decode('utf-8')

    return hex_payload