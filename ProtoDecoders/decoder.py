#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import binascii
import subprocess

from google.protobuf import text_format
import datetime
import pytz

from ProtoDecoders import DeviceUpdate_pb2, LocationReportsUpload_pb2
from example_data_provider import get_example_data


# Custom message formatter to print the Protobuf byte fields as hex strings
def custom_message_formatter(message, indent, as_one_line):
    lines = []
    indent = f"{indent}"
    indent = indent.removeprefix("0")

    for field, value in message.ListFields():
        if field.type == field.TYPE_BYTES:
            hex_value = binascii.hexlify(value).decode('utf-8')
            lines.append(f"{indent}{field.name}: \"{hex_value}\"")
        elif field.type == field.TYPE_MESSAGE:
            if field.label == field.LABEL_REPEATED:
                for sub_message in value:
                    if field.message_type.name == "Time":
                        # Convert Unix time to human-readable format
                        unix_time = sub_message.seconds
                        local_time = datetime.datetime.fromtimestamp(unix_time, pytz.timezone('Europe/Berlin'))
                        lines.append(f"{indent}{field.name} {{\n{indent}  {local_time}\n{indent}}}")
                    else:
                        nested_message = custom_message_formatter(sub_message, f"{indent}  ", as_one_line)
                        lines.append(f"{indent}{field.name} {{\n{nested_message}\n{indent}}}")
            else:
                if field.message_type.name == "Time":
                    # Convert Unix time to human-readable format
                    unix_time = value.seconds
                    local_time = datetime.datetime.fromtimestamp(unix_time, pytz.timezone('Europe/Berlin'))
                    lines.append(f"{indent}{field.name} {{\n{indent}  {local_time}\n{indent}}}")
                else:
                    nested_message = custom_message_formatter(value, f"{indent}  ", as_one_line)
                    lines.append(f"{indent}{field.name} {{\n{nested_message}\n{indent}}}")
        else:
            lines.append(f"{indent}{field.name}: {value}")
    return "\n".join(lines)


def parse_location_report_upload_protobuf(hex_string):
    locationReports = LocationReportsUpload_pb2.LocationReportsUpload()
    locationReports.ParseFromString(bytes.fromhex(hex_string))
    return locationReports


def parse_device_update_protobuf(hex_string):
    deviceUpdate = DeviceUpdate_pb2.DeviceUpdate()
    deviceUpdate.ParseFromString(bytes.fromhex(hex_string))
    return deviceUpdate


def parse_device_list_protobuf(hex_string):
    deviceList = DeviceUpdate_pb2.DevicesList()
    deviceList.ParseFromString(bytes.fromhex(hex_string))
    return deviceList


def get_canonic_ids(device_list):
    result = []
    for device in device_list.deviceMetadata:
        if device.identifierInformation.type == DeviceUpdate_pb2.IDENTIFIER_ANDROID: 
            canonic_ids = device.identifierInformation.phoneInformation.canonicIds.canonicId
        else:
            canonic_ids = device.identifierInformation.canonicIds.canonicId
        device_name = device.userDefinedDeviceName
        for canonic_id in canonic_ids:
            result.append((device_name, canonic_id.id))
    return result


def print_location_report_upload_protobuf(hex_string):
    print(text_format.MessageToString(parse_location_report_upload_protobuf(hex_string), message_formatter=custom_message_formatter))


def print_device_update_protobuf(hex_string):
    print(text_format.MessageToString(parse_device_update_protobuf(hex_string), message_formatter=custom_message_formatter))


def print_device_list_protobuf(hex_string):
    print(text_format.MessageToString(parse_device_list_protobuf(hex_string), message_formatter=custom_message_formatter))


if __name__ == '__main__':
    # Recompile
    subprocess.run(["protoc", "--python_out=.", "ProtoDecoders/Common.proto"], cwd="../")
    subprocess.run(["protoc", "--python_out=.", "ProtoDecoders/DeviceUpdate.proto"], cwd="../")
    subprocess.run(["protoc", "--python_out=.", "ProtoDecoders/LocationReportsUpload.proto"], cwd="../")

    subprocess.run(["protoc", "--pyi_out=.", "ProtoDecoders/Common.proto"], cwd="../")
    subprocess.run(["protoc", "--pyi_out=.", "ProtoDecoders/DeviceUpdate.proto"], cwd="../")
    subprocess.run(["protoc", "--pyi_out=.", "ProtoDecoders/LocationReportsUpload.proto"], cwd="../")

    print("\n ------------------- \n")

    print("Device List: ")
    print_device_list_protobuf(get_example_data("sample_nbe_list_devices_response"))

    print("Own Report: ")
    print_location_report_upload_protobuf(get_example_data("sample_own_report"))

    print("\n ------------------- \n")

    print("Not Own Report: ")
    print_location_report_upload_protobuf(get_example_data("sample_foreign_report"))

    print("\n ------------------- \n")

    print("Device Update: ")
    print_device_update_protobuf(get_example_data("sample_device_update"))
