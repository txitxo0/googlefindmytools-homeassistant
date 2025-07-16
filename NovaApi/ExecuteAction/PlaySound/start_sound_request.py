#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#
from auth.fcm_receiver import FcmReceiver
from NovaApi.ExecuteAction.PlaySound.sound_request import create_sound_request
from NovaApi.nova_request import nova_request
from NovaApi.scopes import NOVA_ACTION_API_SCOPE
from example_data_provider import get_example_data


def start_sound_request(canonic_device_id, gcm_registration_id):
    return create_sound_request(True, canonic_device_id, gcm_registration_id)


if __name__ == '__main__':
    sample_canonic_device_id = get_example_data("sample_canonic_device_id")

    fcm_token = FcmReceiver().register_for_location_updates( lambda x: print(x) )

    hex_payload = start_sound_request(sample_canonic_device_id, fcm_token)
    nova_request(NOVA_ACTION_API_SCOPE, hex_payload)