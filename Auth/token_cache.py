#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import json
import os

def get_cached_value(name, generator):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    secrets_file = os.path.join(script_dir, 'secrets.json')

    if os.path.exists(secrets_file):
        with open(secrets_file, 'r') as file:
            try:
                data = json.load(file)
                value = data.get(name)
                if value:
                    print("[TokenCache] Using cached " + name)
                    return value
            except json.JSONDecodeError:
                print("[TokenCache] Could not parse secrets.json. Need to overwrite file.")
                value = generator()
                data = {name: value}
                with open(secrets_file, 'w') as file:
                    json.dump(data, file)
                return value


    print("[TokenCache] " + name + " does not exist in cache. Creating new...")
    value = generator()
    if os.path.exists(secrets_file):
        with open(secrets_file, 'r') as file:
            data = json.load(file)
    else:
        data = {}
    data[name] = value
    with open(secrets_file, 'w') as file:
        json.dump(data, file)

    return value