#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from NovaApi.ExecuteAction.nbe_execute_action import create_action_request, serialize_action_request
from ProtoDecoders import DeviceUpdate_pb2

def create_sound_request(should_start, canonic_device_id, gcm_registration_id):

    actionRequest = create_action_request(canonic_device_id, gcm_registration_id)

    if should_start:
        actionRequest.action.startSound.component = DeviceUpdate_pb2.DeviceComponent.DEVICE_COMPONENT_UNSPECIFIED
    else:
        actionRequest.action.stopSound.component = DeviceUpdate_pb2.DeviceComponent.DEVICE_COMPONENT_UNSPECIFIED

    return serialize_action_request(actionRequest)