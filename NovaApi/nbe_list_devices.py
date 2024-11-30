import binascii

from NovaApi.common_request import nova_request
from NovaApi.util import generate_random_uuid
from ProtoDecoders import DeviceUpdate_pb2
from ProtoDecoders.decoder import print_device_list_protobuf

def request_device_list():

    hex_payload = create_device_list_request()
    result = nova_request("nbe_list_devices", hex_payload)

    print_device_list_protobuf(result)


def create_device_list_request():
    wrapper = DeviceUpdate_pb2.DevicesListRequest()

    # Query for Spot devices
    wrapper.deviceListRequestPayload.type = DeviceUpdate_pb2.DeviceType.SPOT_DEVICE

    # Set a random UUID as the request ID
    wrapper.deviceListRequestPayload.id = generate_random_uuid()

    # Serialize to binary string
    binary_payload = wrapper.SerializeToString()

    # Convert to hex string
    hex_payload = binascii.hexlify(binary_payload).decode('utf-8')

    return hex_payload


if __name__ == '__main__':
    request_device_list()
