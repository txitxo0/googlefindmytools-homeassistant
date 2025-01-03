# GoogleFindMyTools

This repository includes some useful tools for understanding how Google's Find My Device Network works. It will be extended over time.

### What's possible?
Currently, it is possible to query Find My Device trackers and their corresponding decrypted locations.

### How to use
- All packages in requirements.txt need to be installed: `pip install -r requirements.txt`
- Google Chrome needs to be installed on your system.

- You can try out this code by running main.py: `python main.py`

### Known Issues
- First registration for Cloud Messaging takes a while, be patient.
- There seem to be issues with the package "undetected-chromedriver" not detecting Chrome on Windows and ARM Linux. macOS is working fine.
