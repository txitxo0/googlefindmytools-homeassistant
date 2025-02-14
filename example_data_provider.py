#
#  GoogleFindMyTools - A set of tools to interact with the Google Find My API
#  Copyright © 2024 Leon Böttger. All rights reserved.
#

import json
import os

def get_example_data(identifier: str) -> str:
    try:
        with open(_get_example_file(), 'r') as file:
            data = json.load(file)
            value = data.get(identifier)

            if value is not None:
                return value
            else:
                raise ValueError("The requested value was not found in the example data file (example_data.json).")
    except Exception:
        raise ValueError("The requested value was not found in the example data file (example_data.json). Please make sure the file is present and correctly formatted.")


def _get_example_file() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'example_data.json')