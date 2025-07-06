# Google Find My Tools for Home Assistant 📍

Tired of wondering where your Google Find My-enabled devices are? 🤔 This project brings the power of Google's Find My Device network right into your Home Assistant dashboard! 🏠✨

It periodically fetches the location of your trackers (like Chipolo, Pebblebee, etc.) and publishes them to an MQTT broker, with auto-discovery for Home Assistant.

## ⭐ Features

- 🔎 Fetches location data for your Google Find My network devices.
- 🛰️ Publishes device locations via MQTT.
- 🤖 Supports Home Assistant MQTT Discovery for seamless integration.
- ⚙️ Highly configurable through environment variables.
- 🐳 Docker-friendly for easy deployment.

## 🚦 Prerequisites

- A running MQTT Broker (like Mosquitto).
- A Google Account with Find My devices paired.

## 🛠️ Setup & Installation

### 1. Authentication (One-Time Step)

To use this tool, you first need to obtain your Google authentication credentials. This is a manual process that requires a graphical environment.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/GoogleFindMyTools-homeassistant.git
    cd GoogleFindMyTools-homeassistant
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the authentication script:**
    ```bash
    python main.py
    ```
    - A Chrome window will open.
    - **Log in to your Google account** and complete any 2-Factor Authentication steps.
    - The script will create a `Auth/secrets.json` file. This file contains the necessary credentials for the script to run.

### 2. Docker Deployment

This is the recommended way to run the tool after the initial authentication.

**`docker-compose.yml`:**

```yaml
services:
  google-find-my-tools:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: google-find-my-tools
    restart: unless-stopped
    volumes:
      - ./Auth/secrets.json:/app/Auth/secrets.json:ro
    # Environment variables can be set in a .env file
    # MQTT_BROKER=your_broker_ip
    # MQTT_USERNAME=your_mqtt_user
    # MQTT_PASSWORD=your_mqtt_password
```

**To run:**

1.  Make sure you have the `Auth/secrets.json` file from the authentication step.
2.  Create a `.env` file in the same directory as the `docker-compose.yml` file with your MQTT credentials.
3.  Run `docker-compose up -d`.

**`docker run` command:**

```bash
docker run -d \
  --name=google-find-my-tools \
  -e MQTT_BROKER="your_broker_ip" \
  -e MQTT_USERNAME="your_mqtt_user" \
  -e MQTT_PASSWORD="your_mqtt_password" \
  -e REFRESH_INTERVAL="600" \
  -e DEVICE_NAMES_FILTER="My Keys,My Backpack" \
  -v $(pwd)/Auth/secrets.json:/app/Auth/secrets.json:ro \
  --restart unless-stopped \
  google-find-my-tools
```

## ⚙️ Configuration

The application is configured using environment variables.

| Variable              | Description                                                                                                   | Default                               | Required |
| --------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------- | -------- |
| `MQTT_BROROKER`         | The address of your MQTT broker (e.g., `192.168.1.100` or `mqtt.local`).                                       | -                                     | **Yes**  |
| `MQTT_PORT`           | The port for your MQTT broker.                                                                                | `1883`                                | No       |
| `MQTT_USERNAME`       | The username for your MQTT broker, if authentication is enabled.                                              | -                                     | No       |
| `MQTT_PASSWORD`       | The password for your MQTT broker, if authentication is enabled.                                              | -                                     | No       |
| `MQTT_CLIENT_ID`      | A custom client ID for connecting to MQTT. A random suffix is added to prevent collisions.                    | `google_find_my_publisher`            | No       |
| `REFRESH_INTERVAL`    | The time in seconds between location updates. 🕒                                                              | `300` (5 minutes)                     | No       |
| `DEVICE_NAMES_FILTER` | A comma-separated list of device names to track. If not set, all devices will be tracked. Example: `My Keys,Wallet` | -                                     | No       |

## 🚀 Usage (Local)

The script requires a one-time manual login to create a persistent session.

### 1. First-Time Authentication (One-Time Step)

Run the `main.py` script to authorize the application with your Google Account.

```bash
python main.py
```

- A Chrome window will open.
- **Log in to your Google account** and complete any 2-Factor Authentication steps.
- The script will list your devices in the console and then exit. Your session is now saved.

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

**IMPORTANT:** You must first generate a Chrome user profile with a valid Google session on your local machine (with a graphical interface).

1.  **Generate Session Data (One-Time Setup):**
    a. On your local computer, run the authentication script: `python main.py`.
    b. A Chrome window will open. **Log in to your Google Account**. The script will exit after listing your devices.
    c. This creates a user profile folder. The location depends on your OS:
       - **Linux:** `~/.config/undetected_chromedriver`
       - **Windows:** `%LOCALAPPDATA%\undetected_chromedriver`
       - **macOS:** `~/Library/Application Support/undetected_chromedriver`
    d. Copy the contents of this folder into a local directory for the Docker context, for example, `./user_data`. This is your persistent session data.

2.  **Build the Docker image:**
    ```bash
    docker build -t google-find-my-tools .
    ```

3.  **Run the container:**
    Run the container, mounting the `user_data` directory. Note the updated volume path (`/home/appuser/...`) which is required for the more secure non-root user inside the container.

    ```bash
    docker run -d \
      --name=google-find-my-tools \
      -e MQTT_BROKER="your_broker_ip" \
      -e MQTT_USERNAME="your_mqtt_user" \
      -e MQTT_PASSWORD="your_mqtt_password" \
      -e REFRESH_INTERVAL="600" \
      -e DEVICE_NAMES_FILTER="My Keys,My Backpack" \
      -v ./user_data:/home/appuser/.config/undetected_chromedriver \
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
