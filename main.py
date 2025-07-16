#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

from NovaApi.ListDevices.nbe_list_devices import list_devices
from auth.fcm_receiver import FcmReceiver

if __name__ == '__main__':
    try:
        list_devices()
    finally:
        # Ensure the FCM receiver connection is closed
        FcmReceiver().stop_listening()