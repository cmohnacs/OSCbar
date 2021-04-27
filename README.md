# OSCbar
Calibration oscillator for the macOS menu bar

## Features
OSCbar lives in the macOS menu bar and functions as an on-hand oscillator for calibrating/testing audio equipment or room response.  It is designed to be a lighweight and accessible sound generator.  Thes feature set is intentionally minimal to replace those circustamces when opening a DAW is overkill.

Maximum amplitude is determined by your device's interface.

Freq range: 20 - 20k Hz

![alt text](https://github.com/cmohnacs/oscbar/blob/main/media/appview.png?raw=true)

#### Wave Types
- Sine wave
- Square wave
- White noise
- Pink noise

#### Callibration modes
Use octave walks to check the low-end response of your studio or listening room.

## About
The application uses ```sounddevice``` and ```rumps``` libraries.  ```oscillator.py``` is an oscillator class that can be implemented in other ```sounddevice``` applications.

## Install
Visit the [project page](https://cmohnacs.github.io/oscbar/) to download ```oscbar.app```.

