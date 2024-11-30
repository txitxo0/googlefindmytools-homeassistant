from NovaApi.ExecuteAction.nbe_execute_action import create_action_request, serialize_action_request
from NovaApi.common_request import nova_request
from NovaApi.scopes import NOVA_ACTION_API_SCOPE
from ProtoDecoders import DeviceUpdate_pb2
from private import sample_gcm_registration_id, sample_canonic_device_id


def create_location_request(canonic_device_id, gcm_registration_id):

    actionRequest = create_action_request(canonic_device_id, gcm_registration_id)

    # Random values, can be arbitrary
    actionRequest.action.locateTracker.activationDate.seconds = 1732120060
    actionRequest.action.locateTracker.activationDate.nanos = 0

    actionRequest.action.locateTracker.contributorType = DeviceUpdate_pb2.SpotContributorType.FMDN_ALL_LOCATIONS

    # Convert to hex string
    hex_payload = serialize_action_request(actionRequest)

    return hex_payload


if __name__ == '__main__':
    hex_payload = create_location_request(sample_canonic_device_id, sample_gcm_registration_id)
    nova_request(NOVA_ACTION_API_SCOPE, hex_payload)
