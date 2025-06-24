# Google Find My Tools for Home Assistant

This project is a fork of [GoogleFindMyTools by leonboe1](https://github.com/leonboe1/GoogleFindMyTools) adapted to publish Google Find My Device locations to an MQTT broker for integration with [Home Assistant](https://www.home-assistant.io/).

It retrieves the location of your registered devices (phones, watches, trackers) from Google's Find My Device network and publishes them via MQTT, allowing Home Assistant to automatically discover and display them as `device_tracker` entities.

## How it works

The script uses an undocumented Google API to fetch device information and location data. It then connects to your MQTT broker and publishes the data in a format compatible with Home Assistant's MQTT Discovery feature.

## Setup

### Prerequisites

*   Python 3.10 or newer.
*   A recent version of Google Chrome installed.
*   An MQTT broker (like the Mosquitto add-on in Home Assistant).

### Installation

1.  Clone this repository:
    ```bash
    git clone https://github.com/your-repo/GoogleFindMyTools-homeassistant.git
    cd GoogleFindMyTools-homeassistant
    ```

2.  Install the required Python packages:

    It is highly recommended to use a Python virtual environment.
    ```bash
    # Create a virtual environment
    python -m venv venv
    
    # Activate it (the command depends on your OS)
    # On Windows (in Command Prompt or PowerShell)
    .\venv\Scripts\activate
    # On Linux/macOS
    source venv/bin/activate
    
    # Install dependencies into the virtual environment
    pip install -r requirements.txt
    ```

### Authentication

To use the tools, you need to authenticate with your Google account. The `main.py` script handles this by opening a browser for you to log in, then saving your authentication cookies for future use.

1.  Run the authentication script from the root of the project:
    ```bash
    python main.py
    ```
2.  A Google Chrome window will open. Log in to the Google account associated with your Find My Device network.
3.  After a successful login, the script will automatically create and save the necessary cookies to an `Auth/secrets.json` file.
4.  You only need to do this once. The `publish_mqtt.py` script will use this file for all subsequent runs.

**Important**: The generated `Auth/secrets.json` file contains sensitive authentication tokens. Treat this file like a password and do not share it or commit it to version control.

## Usage

The main script for this integration is `publish_mqtt.py`. It fetches the location for all your devices and publishes them to MQTT.

### Environment Variables

The script is configured using environment variables.

| Variable          | Required | Default                          | Description                                                              |
| ----------------- | -------- | -------------------------------- | ------------------------------------------------------------------------ |
| `MQTT_BROKER`     | **Yes**  | -                                | The hostname or IP address of your MQTT broker.                          |
| `MQTT_PORT`       | No       | `1883`                           | The port number for your MQTT broker.                                    |
| `MQTT_USERNAME`   | No       | -                                | The username for authenticating with the MQTT broker.                    |
| `MQTT_PASSWORD`   | No       | -                                | The password for authenticating with the MQTT broker.                    |
| `MQTT_CLIENT_ID`  | No       | `google_find_my_publisher_...`   | The client ID to use when connecting to MQTT. A random one is generated. |

### Running the script

Set the required environment variables and run the script.

**Example (Linux/macOS):**

```bash
export MQTT_BROKER="192.168.1.100"
export MQTT_USERNAME="my-mqtt-user"
export MQTT_PASSWORD="my-mqtt-password"
python publish_mqtt.py
```

**Example (Windows - Command Prompt):**

```powershell
$env:MQTT_BROKER="192.168.1.100"
$env:MQTT_PORT="192.168.1.100"
$env:MQTT_USERNAME="my-mqtt-user"
$env:MQTT_PASSWORD="my-mqtt-password"
python publish_mqtt.py
```

**Example (Windows - PowerShell):**

```powershell
$env:MQTT_BROKER="192.168.1.100"
$env:MQTT_USERNAME="my-mqtt-user"
$env:MQTT_PASSWORD="my-mqtt-password"
python publish_mqtt.py
```

You can run this script periodically (e.g., using a cron job or a systemd timer) to keep the device locations updated in Home Assistant.

## Home Assistant Integration

If MQTT Discovery is enabled in your Home Assistant configuration (it is by default), the devices will appear automatically after the script runs for the first time.

*   Each device will be created as a `device_tracker` entity (e.g., `device_tracker.google_find_my_pixel_8_pro`).
*   The state of the tracker will be `unknown` as this script only provides GPS coordinates, not zone information. You can use Home Assistant zones to determine if a device is `home` or `not_home`.
*   The device will have attributes such as `latitude`, `longitude`, `gps_accuracy`, and `last_updated`.

## Acknowledgements

This project is heavily based on the work of Leon Böttger in his GoogleFindMyTools repository.