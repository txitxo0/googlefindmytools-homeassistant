#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import datetime
from binascii import unhexlify

from FMDNCrypto.LocationReporting.foreign_tracker_encryptor import decrypt
from KeyBackup.cloud_key_decryptor import decrypt_eik
from NovaApi.ExecuteAction.LocateTracker.decrypted_location import EncryptedLocation
from ProtoDecoders import DeviceUpdate_pb2
from ProtoDecoders.decoder import parse_device_update_protobuf
from SpotApi.GetEidInfoForE2eeDevices.get_owner_key import get_owner_key


def decrypt_location_response_locations(device_update_protobuf):

    encrypted_identity_key = device_update_protobuf.deviceMetadata.information.ephemeralDeviceInformation.encryptedKeys.encryptedIdentityKey
    owner_key = get_owner_key()

    identity_key = decrypt_eik(unhexlify(owner_key), encrypted_identity_key.hex())

    print(identity_key.hex())

    network_locations = device_update_protobuf.deviceMetadata.information.locationInformation.reports.recentLocationAndNetworkLocations.networkLocations
    network_locations_time = device_update_protobuf.deviceMetadata.information.locationInformation.reports.recentLocationAndNetworkLocations.networkLocationTimestamps

    location_time_array = []
    for loc, time in zip(network_locations, network_locations_time):

        encrypted_location_hex = loc.locationAndDeviceTimeOffset.encryptedReport.encryptedLocation
        public_key_random = loc.locationAndDeviceTimeOffset.encryptedReport.publicKeyRandom
        time_offset = loc.locationAndDeviceTimeOffset.deviceTimeOffset

        decrypted_location = decrypt(identity_key.hex(), encrypted_location_hex, public_key_random, time_offset)

        encrypted_location = EncryptedLocation(
            decrypted_location=decrypted_location,
            time=int(time.seconds),
            accuracy=loc.locationAndDeviceTimeOffset.accuracy,
            status=loc.status,
            is_own_report=loc.locationAndDeviceTimeOffset.encryptedReport.isOwnReport,
        )
        location_time_array.append(encrypted_location)

    print("-" * 40)
    print("[DecryptLocations] Decrypted Locations:")

    for loc in location_time_array:
        proto_loc = DeviceUpdate_pb2.Location()
        proto_loc.ParseFromString(loc.decrypted_location)

        latitude = proto_loc.latitude / 1e7
        longitude = proto_loc.longitude / 1e7
        altitude = proto_loc.altitude

        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print(f"Altitude: {altitude}")
        print(f"Time: {datetime.datetime.fromtimestamp(loc.time).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Status: {loc.status}")
        print(f"Is Own Report: {loc.is_own_report}")
        print("-" * 40)

    print("[NovaApi] Decrypting Locations...")
    pass


if __name__ == '__main__':
    decrypt_location_response_locations(None)