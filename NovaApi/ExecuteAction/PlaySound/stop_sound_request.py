from NovaApi.ExecuteAction.PlaySound.sound_request import create_sound_request
from NovaApi.common_request import nova_request
from NovaApi.scopes import NOVA_ACTION_API_SCOPE
from private import sample_canonic_device_id, sample_gcm_registration_id


def stop_sound_request(canonic_device_id, gcm_registration_id):
    return create_sound_request(False, canonic_device_id, gcm_registration_id)

if __name__ == '__main__':
    hex_payload = stop_sound_request(sample_canonic_device_id, sample_gcm_registration_id)
    nova_request(NOVA_ACTION_API_SCOPE, hex_payload)