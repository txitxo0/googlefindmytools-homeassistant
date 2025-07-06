#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import json



def _transform_to_byte_array(json_object):
    byte_array = bytearray(json_object[str(i)] for i in range(len(json_object)))
    return byte_array


def get_fmdn_shared_key(vault_keys):
    json_object = json.loads(vault_keys)
    processed_data = {}

    # Iterate through the keys in the JSON object
    for key in json_object:
        if key == "finder_hw":
            json_array = json_object[key]
            array_list2 = []

            # Iterate through the JSON array
            for item in json_array:
                epoch = item["epoch"]
                key_data = item["key"]

                processed_key = _transform_to_byte_array(key_data)
                array_list2.append({"epoch": epoch, "key": processed_key})

                return processed_key

            processed_data[key] = array_list2

    raise Exception("No suitable key found in the vault keys.")


