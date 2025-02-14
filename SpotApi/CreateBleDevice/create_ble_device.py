#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import secrets
import time
from binascii import unhexlify

from FMDNCrypto.key_derivation import FMDNOwnerOperations
from FMDNCrypto.eid_generator import ROTATION_PERIOD, generate_eid
from KeyBackup.cloud_key_decryptor import encrypt_aes_gcm
from ProtoDecoders.DeviceUpdate_pb2 import DeviceComponentInformation, SpotDeviceType, RegisterBleDeviceRequest, PublicKeyIdList
from SpotApi.GetEidInfoForE2eeDevices.get_owner_key import get_owner_key
from SpotApi.spot_request import spot_request

mcu_fast_pair_model_id = "003200"

def hours_to_seconds(hours):
    return hours * 3600


def flip_bits(data: bytes, enabled: bool) -> bytes:
    """Flips all bits in each byte of the given byte sequence."""
    if enabled:
        return bytes(b ^ 0xFF for b in data)

    return data


def register_esp32():

    owner_key = unhexlify(get_owner_key())

    eik = secrets.token_bytes(32)
    eid = generate_eid(eik.hex(), 0).to_bytes(length=20, byteorder='big')
    pair_date = int(time.time())

    register_request = RegisterBleDeviceRequest()
    register_request.fastPairModelId = mcu_fast_pair_model_id

    # Description
    register_request.description.userDefinedName = "GoogleFindMyTools µC"
    register_request.description.deviceType = SpotDeviceType.DEVICE_TYPE_BEACON

    # Device Components Information
    component_information = DeviceComponentInformation()
    component_information.imageUrl = "https://m.media-amazon.com/images/I/61o2ZUzB4XL._AC_UF1000,1000_QL80_.jpg"
    register_request.description.deviceComponentsInformation.append(component_information)

    # Capabilities
    register_request.capabilities.isAdvertising = True
    register_request.capabilities.trackableComponents = 1
    register_request.capabilities.capableComponents = 1

    # E2EE Registration
    register_request.e2eePublicKeyRegistration.rotationExponent = 10
    register_request.e2eePublicKeyRegistration.pairingDate = pair_date

    # Encrypted User Secrets
    # Flip bits so Android devices cannot decrypt the key
    register_request.e2eePublicKeyRegistration.encryptedUserSecrets.encryptedIdentityKey = flip_bits(encrypt_aes_gcm(owner_key, eik), True)

    # Random keys, not used for ESP
    register_request.e2eePublicKeyRegistration.encryptedUserSecrets.encryptedAccountKey = secrets.token_bytes(44)
    register_request.e2eePublicKeyRegistration.encryptedUserSecrets.encryptedSha256AccountKeyPublicAddress = secrets.token_bytes(60)

    register_request.e2eePublicKeyRegistration.encryptedUserSecrets.ownerKeyVersion = 1
    register_request.e2eePublicKeyRegistration.encryptedUserSecrets.creationDate.seconds = pair_date

    time_counter = pair_date
    truncated_eid = eid[:10]

    # announce advertisements
    for _ in range(int(hours_to_seconds(3000) / ROTATION_PERIOD)):
        pub_key_id = PublicKeyIdList.PublicKeyIdInfo()
        pub_key_id.publicKeyId.truncatedEid = truncated_eid
        pub_key_id.timestamp.seconds = time_counter
        register_request.e2eePublicKeyRegistration.publicKeyIdList.publicKeyIdInfo.append(pub_key_id)

        time_counter += ROTATION_PERIOD

    # General
    register_request.manufacturerName = "GoogleFindMyTools"
    register_request.modelName = "µC"

    ownerKeys = FMDNOwnerOperations()
    ownerKeys.generate_keys(ephemeral_identity_key_hex=eik.hex())

    register_request.ringKey = ownerKeys.ringing_key
    register_request.recoveryKey = ownerKeys.recovery_key
    register_request.unwantedTrackingKey = ownerKeys.tracking_key

    bytes_data = register_request.SerializeToString()
    spot_request("CreateBleDevice", bytes_data)

    print("Registered device successfully. Copy the Advertisement Key below. It will not be shown again.")
    print("Afterward, go to the folder 'GoogleFindMyTools/ESP32Firmware' or 'GoogleFindMyTools/ZephyrFirmware' and follow the instructions in the README.md file.")

    print("+" + "-" * 78 + "+")
    print("|" + " " * 19 + eid.hex() + " " * 19 + "|")
    print("|" + " " * 30 + "Advertisement Key" + " " * 31 + "|")
    print("+" + "-" * 78 + "+")