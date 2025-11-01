>Repository deprecated in favor of: https://github.com/BSkando/GoogleFindMy-HA
Same roadmap and already achieve and avalaible!




# Google Find My Tools for Home Assistant 📍

Tired of wondering where your Google Find My-enabled devices are? 🤔 This project brings the power of Google's Find My Device network right into your Home Assistant dashboard! 🏠✨

It periodically fetches the location of your trackers (like Chipolo, Pebblebee, etc.) and publishes them to an MQTT broker, with auto-discovery for Home Assistant.

## ⭐ Features

- 🔎 Fetches location data for your Google Find My network devices.
- 🛰️ Publishes device locations via MQTT.
- 🤖 Supports Home Assistant MQTT Discovery for seamless integration.
- ⚙️ Highly configurable through environment variables.
- 🐳 Docker-friendly for easy deployment.
- 🕵️ Uses `undetected-chromedriver` to handle Google's login and bot detection.

## 🚦 Prerequisites

- Python 3.9+
- A running MQTT Broker (like Mosquitto).
- Google Chrome installed on the machine where the script will run (if not using Docker).
- A Google Account with Find My devices paired.

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/txitxo0/googlefindmytools-homeassistant.git
    cd GoogleFindMyTools-homeassistant
    ```

2.  **Install dependencies:**

    There are two sets of dependencies for this project:

    -   **`requirements.txt`**: This file contains the core dependencies needed to run the `publish_mqtt.py` script in a headless environment. It excludes packages like Selenium, which are only needed for the initial authentication step.

        ```bash
        pip install -r requirements.txt
        ```

    -   **`requirements.dev.txt`**: This file includes all dependencies, including those required for the one-time authentication process (like Selenium and `undetected-chromedriver`). You only need this if you are running the authentication flow for the first time.

        ```bash
        pip install -r requirements.dev.txt
        ```

## ⚙️ Configuration

The application is configured using environment variables.

| Variable              | Description                                                                                                   | Default                               | Required |
| --------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------- | -------- |
| `MQTT_BROKER`         | The address of your MQTT broker (e.g., `192.168.1.100` or `mqtt.local`).                                       | -                                     | **Yes**  |
| `MQTT_PORT`           | The port for your MQTT broker.                                                                                | `1883`                                | No       |
| `MQTT_USERNAME`       | The username for your MQTT broker, if authentication is enabled.                                              | -                                     | No       |
| `MQTT_PASSWORD`       | The password for your MQTT broker, if authentication is enabled.                                              | -                                     | No       |
| `MQTT_CLIENT_ID`      | A custom client ID for connecting to MQTT. A random suffix is added to prevent collisions.                    | `google_find_my_publisher`            | No       |
| `REFRESH_INTERVAL`    | The time in seconds between location updates. 🕒                                                              | `300` (5 minutes)                     | No       |
| `DEVICE_NAMES_FILTER` | A comma-separated list of device names to track. If not set, all devices will be tracked. Example: `My Keys,Wallet` | -                                     | No       |
| `SEMANTIC_MAPPING`      | A semicolon-separated list of `key:value` pairs to map semantic locations to Home Assistant zones or specific GPS coordinates. <br> - **Zone Mapping:** `SemanticName:ZoneName` (e.g., `Home:home`) <br> - **Coordinate Mapping:** `SemanticName:latitude,longitude` (e.g., `MomsHouse:37.12345,-122.67890`) <br> - **Mixed Mapping:** `SemanticName:ZoneName;SemanticName:latitude,longitude` (e.g., `Home:home;MomsHouse:37.12345,-122.67890`) | -                                     | No       |

## 🚀 Usage (Local)

The script requires a one-time manual login to create a persistent session.

### 1. First-Time Authentication (One-Time Step)

Run the `main.py` script to authorize the application with your Google Account. Make sure you have installed the development dependencies first:

```bash
pip install -r requirements.dev.txt
python main.py
```

- A Chrome window will open.
- **Log in to your Google account** and complete any 2-Factor Authentication steps.
- The script will list your devices in the console and then exit. Your session is now saved in `auth/secrets.json`.

### 2. Run the Publisher

Once authenticated, set your environment variables and run the main publisher script to start sending data to MQTT.

```bash
# Example for Linux/macOS
export MQTT_BROKER=192.168.1.100
export MQTT_USERNAME=myuser

python publish_mqtt.py
```

## 🐳 Docker Deployment

For a more robust and isolated setup, you can run this tool in a Docker container.

**IMPORTANT:** You must first generate the `auth/secrets.json` file on your local machine (with a graphical interface).

1.  **Generate Session Data (One-Time Setup):**
    a. On your local computer, run the authentication script: `python main.py`.
    b. A Chrome window will open. **Log in to your Google Account**. The script will exit after listing your devices.
    c. This creates the `auth/secrets.json` file.

2.  **Build the Docker image:**
    ```bash
    docker build -t google-find-my-tools .
    ```

3.  **Run the container:**
    Run the container, mounting the `auth` directory.

    ```bash
    docker run -d \
      --name=google-find-my-tools \
      -e MQTT_BROKER="your_broker_ip" \
      -e MQTT_USERNAME="your_mqtt_user" \
      -e MQTT_PASSWORD="your_mqtt_password" \
      -e REFRESH_INTERVAL="600" \
      -e DEVICE_NAMES_FILTER="My Keys,My Backpack" \
      -v ./auth:/app/auth \
      --restart unless-stopped \
      google-find-my-tools
    ```
    The container will now run in headless mode and use your existing login session.

## 🤝 Home Assistant Integration

This script uses the Home Assistant MQTT Discovery protocol.

- Once the script runs successfully and connects to your MQTT broker, your devices will automatically appear as `device_tracker` entities in Home Assistant.
- No further configuration is needed in Home Assistant, as long as MQTT discovery is enabled!

## 🙏 Acknowledgements

This project builds upon the fantastic work of others. A huge thank you to the original authors for their contributions!

-   **leonboe1/GoogleFindMyTools:** The core logic for interacting with Google's Find My Device API and the authentication script (`main.py`) are based on this repository.
-   **endeavour/GoogleFindMyTools-homeassistant:** The Home Assistant integration, including MQTT discovery and publishing logic, is adapted from this project.

---

*Disclaimer: This project is not affiliated with or endorsed by Google. Use it at your own risk.*
