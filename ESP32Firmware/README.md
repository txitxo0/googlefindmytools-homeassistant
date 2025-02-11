# Find My Device ESP32 Firmware

This code enables you to use an ESP32-device as a custom Google Find My Device tracker. Note that the firmware is very experimental.

The firmware works differently to regular Find My Device trackers. It is made to be as simple as possible. It has no Fast Pair support, MAC rotation, advertisement rotation, etc.


## How to use

- Run the Python Script [`main.py`](../main.py) in the parent folder. Follow the instructions of the [README of the parent folder](../README.md).
- When the device list is displayed, press 'r' to register a new ESP32 device in your account. Copy the displayed advertisement key.
- Install Visual Studio Code [here](https://code.visualstudio.com/download)
- Go to Visual Studio Code Extensions, search, install and open 'ESP-IDF' by Espressif
- Open the folder containing this README file in Visual Studio Code
- Navigate to the folder main, select the file [`main.c`](main/main.c)
- Edit Line 15, and insert the advertisement key retrieved from the Python Script
- Connect your ESP32 to your system with USB
- On the bottom left of Visual Studio Code, click the 'plug' icon and select your ESP32, it should be named '/dev/tty.usbserial-0001' or similar
- Click the 'Fire' icon to build and flash the firmware
- If asked, use UART as flash method
- After flashing, the ESP32 will restart and start advertising as the Find My Device tracker previously registered


## Known Issues

- **You might need to re-register the ESP32 after 3 days** (working on a fix)
- Might not work with 'fresh' Google accounts, make sure that you used the Find My Device app on an Android device before registering a new tracker
- You cannot view locations for the ESP32 in the Google Find My Device app. You will need to use the Python script to do so.
- No privacy features such as rotating MAC addresses are implemented
- The firmware was built to receive as many network reports as possible. Therefore, it might consume more power than necessary. To fix this, you can tweak the parameters (TX Power and advertising interval) in [`main.c`](main/main.c)
