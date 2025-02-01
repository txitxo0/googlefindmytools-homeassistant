# GoogleFindMyTools

This repository includes some useful tools for understanding how Google's Find My Device Network works. It will be extended over time. Note that the code of this repo is still very experimental.

### What's possible?
Currently, it is possible to query Find My Device trackers and Android devices, read out their E2EE keys, and decrypt encrypted locations sent from the Find My Device network. You can also send commands to your trackers over the network, such as ringing the tracker.

### How to use
- All packages in requirements.txt need to be installed: `pip install -r requirements.txt`
- Google Chrome needs to be installed on your system.
- You can try out this code by running main.py: `python main.py`

### Known Issues
- First registration for Cloud Messaging takes a while, be patient.
- There seem to be issues with the package "undetected-chromedriver" not detecting Chrome on Windows and ARM Linux. macOS is working fine.
- No support for trackers using the P-256 curve and 32-Byte advertisements. Regular trackers don't seem to use this curve at all - I can only confirm that it is used with Sony's WH1000XM5 headphones. 
