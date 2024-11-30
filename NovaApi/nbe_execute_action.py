import binascii

from NovaApi.common_request import nova_request
from NovaApi.util import generate_random_uuid
from ProtoDecoders import DeviceUpdate_pb2
from private import sample_canonic_device_id, sample_gcm_registration_id

API_SCOPE = "nbe_execute_action"
client_id = generate_random_uuid()

def perform_action():
    while True:
        action = input("Enter 1 to start sound, 2 to stop sound, or q to quit: ")
        if action == '1':
            hex_payload = start_sound_request(sample_canonic_device_id, sample_gcm_registration_id)
            nova_request(API_SCOPE, hex_payload)
        elif action == '2':
            hex_payload = stop_sound_request(sample_canonic_device_id, sample_gcm_registration_id)
            nova_request(API_SCOPE, hex_payload)
        elif action.lower() == 'q':
            break
        else:
            print("Invalid input. Please enter 1, 2, or q.")


def start_sound_request(canonic_device_id, gcm_registration_id):
    return create_sound_request(True, canonic_device_id, gcm_registration_id)


def stop_sound_request(canonic_device_id, gcm_registration_id):
    return create_sound_request(False, canonic_device_id, gcm_registration_id)


def create_sound_request(should_start, canonic_device_id, gcm_registration_id):
    actionRequest = DeviceUpdate_pb2.ExecuteActionRequest()

    actionRequest.scope.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    actionRequest.scope.device.canonicId.id = canonic_device_id

    if should_start:
        actionRequest.action.makeSound.component = DeviceUpdate_pb2.DeviceComponent.DEVICE_COMPONENT_UNSPECIFIED
    else:
        actionRequest.action.stopSound.component = DeviceUpdate_pb2.DeviceComponent.DEVICE_COMPONENT_UNSPECIFIED

    actionRequest.requestMetadata.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE
    actionRequest.requestMetadata.requestUuid = generate_random_uuid()
    actionRequest.requestMetadata.fmdClientUuid = client_id
    actionRequest.requestMetadata.gcmRegistrationId.id = gcm_registration_id
    actionRequest.requestMetadata.isValid = True

    # Serialize to binary string
    binary_payload = actionRequest.SerializeToString()

    # Convert to hex string
    hex_payload = binascii.hexlify(binary_payload).decode('utf-8')

    return hex_payload


if __name__ == '__main__':
    perform_action()
