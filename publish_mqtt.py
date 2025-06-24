import json
import logging
import os
import time
from typing import Dict

import paho.mqtt.client as mqtt
import petname

from NovaApi.ExecuteAction.LocateTracker.location_request import (
    get_location_data_for_device,
)
from NovaApi.ListDevices.nbe_list_devices import request_device_list
from ProtoDecoders.decoder import get_canonic_ids, parse_device_list_protobuf

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("GoogleFindMyTools")

# MQTT Configuration
MQTT_BROKER = os.environ["MQTT_BROKER"]  # Default to localhost if not set
MQTT_PORT = int(os.environ.get("MQTT_PORT", 1883))
MQTT_USERNAME = os.environ.get("MQTT_USERNAME")  # Set your MQTT username if required
MQTT_PASSWORD = os.environ.get("MQTT_PASSWORD")  # Set your MQTT password if required
MQTT_CLIENT_ID = f"{os.environ.get('MQTT_CLIENT_ID', 'google_find_my_publisher')}_{petname.Generate(3, '')}"

# Home Assistant MQTT Discovery
DISCOVERY_PREFIX = "homeassistant"
DEVICE_PREFIX = "google_find_my"


def on_connect(client, userdata, flags, result_code, properties):
    """Callback when connected to MQTT broker"""
    if result_code == 0:
        logger.info("Successfully connected to the MQTT broker.")
    else:
        logger.error(
            f"Failed to connect to the MQTT broker. Result code: {result_code}"
        )


def publish_device_config(
    client: mqtt.Client, device_name: str, canonic_id: str
) -> None:
    """Publish Home Assistant MQTT discovery configuration for a device"""
    base_topic = f"{DISCOVERY_PREFIX}/device_tracker/{DEVICE_PREFIX}_{canonic_id}"

    # Device configuration for Home Assistant
    config = {
        "unique_id": f"{DEVICE_PREFIX}_{canonic_id}",
        "state_topic": f"{base_topic}/state",
        "json_attributes_topic": f"{base_topic}/attributes",
        "source_type": "gps",
        "device": {
            "identifiers": [f"{DEVICE_PREFIX}_{canonic_id}"],
            "name": device_name,
            "model": "Google Find My Device",
            "manufacturer": "Google",
        },
    }
    logger.info(
        f"Publishing discovery configuration for '{device_name}' (ID: {canonic_id}) to topic '{base_topic}/config'."
    )
    # Publish discovery config
    r = client.publish(f"{base_topic}/config", json.dumps(config), retain=True)
    return r


def publish_device_state(
    client: mqtt.Client, device_name: str, canonic_id: str, location_data: Dict
) -> None:
    """Publish device state and attributes to MQTT"""
    base_topic = f"{DISCOVERY_PREFIX}/device_tracker/{DEVICE_PREFIX}_{canonic_id}"

    # Extract location data
    lat = location_data.get("latitude")
    lon = location_data.get("longitude")
    accuracy = location_data.get("accuracy")
    altitude = location_data.get("altitude")
    timestamp = location_data.get("timestamp", time.time())

    # Publish state (home/not_home/unknown)
    state = "unknown"
    client.publish(f"{base_topic}/state", state)

    # Publish attributes
    attributes = {
        "latitude": lat,
        "longitude": lon,
        "altitude": altitude,
        "gps_accuracy": accuracy,
        "source_type": "gps",
        "last_updated": timestamp,
    }
    logger.info(
        f"Publishing location for '{device_name}' (ID: {canonic_id}): "
        f"lat={lat}, lon={lon}, accuracy={accuracy}, altitude={altitude}, timestamp={timestamp}"
    )
    r = client.publish(f"{base_topic}/attributes", json.dumps(attributes))
    return r


def main():
    # Initialize MQTT client
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
    client.on_connect = on_connect

    if MQTT_USERNAME:
        client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

    try:
        logger.info("Connecting to the MQTT broker...")
        client.connect(MQTT_BROKER, MQTT_PORT)
        client.loop_start()

        logger.info("Retrieving device list from Google Find My Device API...")
        result_hex = request_device_list()
        device_list = parse_device_list_protobuf(result_hex)
        canonic_ids = get_canonic_ids(device_list)

        logger.info(f"Found {len(canonic_ids)} device(s) to publish.")

        # Publish discovery config and state for each device
        for device_name, canonic_id in canonic_ids:
            logger.info(f"Processing device '{device_name}' (ID: {canonic_id})...")

            # Publish discovery configuration
            msg_info = publish_device_config(client, device_name, canonic_id)
            msg_info.wait_for_publish()

            # Get and publish location data
            location_data = get_location_data_for_device(canonic_id, device_name)
            msg_info = publish_device_state(
                client, device_name, canonic_id, location_data
            )
            msg_info.wait_for_publish()

            logger.info(f"Finished publishing data for '{device_name}'.")

        logger.info("All devices have been published to MQTT.")
        logger.info("Devices should now be discoverable in Home Assistant.")
        logger.info(
            "If you don't see them, try restarting Home Assistant or triggering device discovery."
        )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        client.loop_stop()
        client.disconnect()
        logger.info("Disconnected from the MQTT broker.")


if __name__ == "__main__":
    main()
