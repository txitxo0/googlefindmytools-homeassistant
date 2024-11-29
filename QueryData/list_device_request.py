import binascii
import uuid

import requests

from ProtoDecoders import DeviceUpdate_pb2
from ProtoDecoders.decoder import print_device_list_protobuf
from private import sample_android_device_manager_oauth_token

def request_device_list():
    url = "https://android.googleapis.com/nova/nbe_list_devices"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Authorization": "Bearer " + sample_android_device_manager_oauth_token, # Insert your OAuth token here
        "Accept-Language": "en-US",
        "User-Agent": "fmd/20006320; gzip"
    }

    # Required to get SPOT devices as well
    hex_payload = create_device_list_request()
    payload = binascii.unhexlify(hex_payload)

    response = requests.post(url, headers=headers, data=payload)
    print("Status Code:", response.status_code)
    print_device_list_protobuf(response.content.hex())

    return response


def create_device_list_request():
    wrapper = DeviceUpdate_pb2.DevicesListRequest()

    # 2 = Include SPOT devices
    wrapper.deviceListRequestPayload.type = 2

    # Generate a random UUID
    random_uuid = uuid.uuid4()

    # Convert the UUID to a string
    uuid_str = str(random_uuid)

    # Set the UUID as the request ID
    wrapper.deviceListRequestPayload.id = uuid_str

    # Serialize to binary string
    binary_payload = wrapper.SerializeToString()

    # Convert to hex string
    hex_payload = binascii.hexlify(binary_payload).decode('utf-8')

    return hex_payload


if __name__ == '__main__':
    request_device_list()
