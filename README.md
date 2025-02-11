# GoogleFindMyTools

This repository includes some useful tools that reimplement parts of Google's Find My Device Network. Note that the code of this repo is still very experimental.

### What's possible?
Currently, it is possible to query Find My Device trackers and Android devices, read out their E2EE keys, and decrypt encrypted locations sent from the Find My Device network. You can also send register your own ESP32-based trackers, as described below.

### How to use
- All packages in requirements.txt need to be installed: `pip install -r requirements.txt`
- Google Chrome needs to be installed on your system.
- You can try out this code by running [main.py](main.py): `python main.py`

### Known Issues
- There seem to be issues with the package "undetected-chromedriver" not detecting Chrome on Windows and ARM Linux. macOS is working fine.
- No support for trackers using the P-256 curve and 32-Byte advertisements. Regular trackers don't seem to use this curve at all - I can only confirm that it is used with Sony's WH1000XM5 headphones.

### Firmware for custom ESP32-based trackers
If you want to use an ESP32 as a custom Find My Device tracker, you can find the firmware in the folder ESP32Firmware. To register a new tracker, run main.py and press 'r' if you are asked to. Afterward, follow the instructions on-screen.

For more information, check the [README in the ESP32Firmware folder](ESP32Firmware/README.md).
