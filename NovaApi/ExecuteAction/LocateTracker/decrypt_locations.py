#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import datetime
import hashlib
from binascii import unhexlify

from FMDNCrypto.LocationReporting.foreign_tracker_encryptor import decrypt
from KeyBackup.cloud_key_decryptor import decrypt_eik, decrypt_aes_gcm
from NovaApi.ExecuteAction.LocateTracker.decrypted_location import WrappedLocation
from ProtoDecoders import DeviceUpdate_pb2
from SpotApi.GetEidInfoForE2eeDevices.get_owner_key import get_owner_key


def decrypt_location_response_locations(device_update_protobuf):

    encrypted_identity_key = device_update_protobuf.deviceMetadata.information.ephemeralDeviceInformation.encryptedKeys.encryptedIdentityKey
    owner_key = get_owner_key()

    identity_key = decrypt_eik(unhexlify(owner_key), encrypted_identity_key.hex())
    locations_proto = device_update_protobuf.deviceMetadata.information.locationInformation.reports.recentLocationAndNetworkLocations

    # At All Areas Reports or Own Reports
    recent_location = locations_proto.recentLocation
    recent_location_time = locations_proto.recentLocationTimestamp

    # High Traffic Reports
    network_locations = list(locations_proto.networkLocations)
    network_locations_time = list(locations_proto.networkLocationTimestamps)

    if locations_proto.HasField("recentLocation"):
        network_locations.append(recent_location)
        network_locations_time.append(recent_location_time)

    location_time_array = []
    for loc, time in zip(network_locations, network_locations_time):

        encrypted_location = loc.locationAndDeviceTimeOffset.encryptedReport.encryptedLocation
        public_key_random = loc.locationAndDeviceTimeOffset.encryptedReport.publicKeyRandom
        time_offset = loc.locationAndDeviceTimeOffset.deviceTimeOffset

        if public_key_random == b"":  # Own Report
            identity_key_hash = hashlib.sha256(identity_key).digest()
            decrypted_location = decrypt_aes_gcm(identity_key_hash, encrypted_location)
        else:
            decrypted_location = decrypt(identity_key.hex(), encrypted_location, public_key_random, time_offset)


        encrypted_location = WrappedLocation(
            decrypted_location=decrypted_location,
            time=int(time.seconds),
            accuracy=loc.locationAndDeviceTimeOffset.accuracy,
            status=loc.status,
            is_own_report=loc.locationAndDeviceTimeOffset.encryptedReport.isOwnReport,
        )
        location_time_array.append(encrypted_location)

    print("-" * 40)
    print("[DecryptLocations] Decrypted Locations:")

    if not location_time_array:
        print("No locations found.")
        return

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

    pass


if __name__ == '__main__':
    decrypt_location_response_locations(None)