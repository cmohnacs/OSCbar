OSCbar lives in the macOS menu bar and functions as an on-hand oscillator for calibrating/testing audio equipment or room response.  It is designed to be a lighweight and accessible sound generator.  Thes feature set is intentionally minimal to replace those circustamces when opening a DAW is overkill.

![alt text](https://github.com/cmohnacs/oscbar/blob/main/media/appview.png?raw=true)

## Features
Generate an waves or noise from the macOS menu bar.  Cmd-click on the icon to rearrange location within the menubar.

#### Wave Types
- Sine wave
- Square wave
- White noise
- Pink noise

**Freq range:** 20 - 20k Hz.

**Callibration modes:** Use octave walks to check the low-end response of your studio or listening room.

Volume displayed dbFS.  Maximum amplitude is determined by your device's interface.


## Technical
The application uses ```sounddevice``` and ```rumps``` libraries.  ```oscillator.py``` is an oscillator class that can be implemented in other ```sounddevice``` applications.  


## Download
Visit the [project page](https://cmohnacs.github.io/oscbar/) to download ```oscbar.app```.

![alt text](https://github.com/cmohnacs/oscbar/blob/main/media/oscbar_logo-250x250.png?raw=true)

### Support or Contact

Get in touch to report bugs or request new features.

