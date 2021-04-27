![alt text](https://github.com/cmohnacs/oscbar/blob/main/media/oscbar_logo-250x250.png?raw=true)

# OSCbar
OSCbar lives in the macOS menu bar and functions as an on-hand oscillator for calibrating/testing audio equipment or room response.  It is designed to be a lighweight and accessible sound generator.  Thes feature set is intentionally minimal to replace those circustamces when opening a DAW is overkill.

![alt text](https://github.com/cmohnacs/oscbar/blob/main/media/appview.png?raw=true)

## Features
Volume displayed dbFS.  Maximum amplitude is determined by your device's interface.

Freq range: 20 - 20k Hz.

#### Wave Types
- Sine wave
- Square wave
- White noise
- Pink noise

#### Callibration modes
Use octave walks to check the low-end response of your studio or listening room.

## Technical
The application uses ```sounddevice``` and ```rumps``` libraries.  ```oscillator.py``` is an oscillator class that can be implemented in other ```sounddevice``` applications.  

Please raise an issue to report bugs or request new features.

## Download
Visit the [project page](https://cmohnacs.github.io/oscbar/) to download ```oscbar.app```.

