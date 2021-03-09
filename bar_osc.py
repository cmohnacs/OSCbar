"""
Bar Osc App

Test oscillator for the macOS menu bar
"""

import math
import rumps
from oscillator import Oscillator

#rumps.debug_mode(True)


# ------------------------------ Helper Functions ------------------------------

def slider_to_freq(value):
    """ convert slider value to frequency (20Hz-20kHz) """
    value *= 0.0001
    return round(math.pow(2, value))

def freq_to_slider(value):
    """ convert frequency (20Hz-20kHz) to slider value """
    value = math.log2(value)
    return value * 10000


# -------------------------------- Menu Bar App --------------------------------

class BarOscApp:
    """ Bar Osc object """

    def __init__(self):
        self.pref = {
            "wave_type": "sine_wave",
            "amplitude": 0.5,
            "frequency": 440
        }
        self.config = {
            "app_name": "Bar Osc",
            "start": "Start Oscillator",
            "stop": "Stop Oscillator",
            "freq": f"Frequency: {self.pref['frequency']}",
            "update": "Check for updates..."
        }
        self.app = rumps.App(self.config["app_name"])

        # set up menu
        self.build_menu()
        self.ready_menu()
        # single oscillator instance for the app
        self.osc = Oscillator(samplerate=44100)

    def build_menu(self):
        """ define menu, buttons, sliders """

        self.start_button = rumps.MenuItem(                 # Start Osc
            title=self.config["start"])
        self.stop_button = rumps.MenuItem(                  # Stop Osc
            title=self.config["stop"])
        self.sine_button = rumps.MenuItem(                  # Sine Wave
            title="Sine Wave",
            callback=None)
        self.square_button = rumps.MenuItem(                # Square Wave
            title="Square Wave",
            callback=self.set_square_wave)
        self.white_noise_button = rumps.MenuItem(           # White Noise
            title="White Noise",
            callback=self.set_white_noise)
        self.freq_title = rumps.MenuItem(                   # Frequency: title
            title=self.config["freq"],
            callback=None)
        self.freq_slider = rumps.SliderMenuItem(            # Frequency slider
            value=freq_to_slider(self.pref["frequency"]),
            min_value=freq_to_slider(20),                   # 20Hz - 20kHz
            max_value=freq_to_slider(20000),
            callback=self.adj_freq,
            dimensions=(180, 20))
        self.check_updates_button = rumps.MenuItem(         # Check for updates
            title=self.config["update"],
            callback=None)

        #populate menu
        self.app.menu = [self.start_button, self.stop_button, None,
            self.sine_button, self.square_button, self.white_noise_button, None,
            self.freq_title, self.freq_slider, None, self.check_updates_button]

    def ready_menu(self):
        """ menu bar while not playing osc """
        self.app.title = "🎛"
        self.start_button.set_callback(self.start_osc)
        self.stop_button.set_callback(None)

    def busy_menu(self):
        """ menu bar while playing osc """
        self.app.title = "🔊"
        self.start_button.set_callback(None)
        self.stop_button.set_callback(self.stop_osc)

    def start_osc(self, sender):
        """ start the oscillator """
        # update menu and title
        self.busy_menu()
        # generate osc tone
        self.osc.play(
            wave_type=self.pref['wave_type'],
            amplitude=self.pref['amplitude'],
            frequency=self.pref['frequency'])

    def stop_osc(self, sender):
        """ stop the oscillator """
        # update menu and title
        self.ready_menu()
        # kill osc tone
        self.osc.stop()

    def set_sine_wave(self, sender):
        self.sine_button.set_callback(None)
        self.square_button.set_callback(self.set_square_wave)
        self.white_noise_button.set_callback(self.set_white_noise)

        self.pref['wave_type'] = 'sine_wave'
        self.osc.stop()
        self.osc.play(
            wave_type=self.pref['wave_type'],
            amplitude=self.pref['amplitude'],
            frequency=self.pref['frequency'])

    def set_square_wave(self, sender):
        self.sine_button.set_callback(self.set_sine_wave)
        self.square_button.set_callback(None)
        self.white_noise_button.set_callback(self.set_white_noise)

        self.pref['wave_type'] = 'square_wave'
        self.osc.stop()
        self.osc.play(
            wave_type=self.pref['wave_type'],
            amplitude=self.pref['amplitude'],
            frequency=self.pref['frequency'])

    def set_white_noise(self, sender):
        self.sine_button.set_callback(self.set_sine_wave)
        self.square_button.set_callback(self.set_square_wave)
        self.white_noise_button.set_callback(None)

        self.pref['wave_type'] = 'white_noise'
        self.osc.stop()
        self.osc.play(
            wave_type=self.pref['wave_type'],
            amplitude=self.pref['amplitude'],
            frequency=self.pref['frequency'])

    def adj_freq(self, sender):
        """ get the oscillator frequency from slider """

        # when slider adjusted, update title and osc freq
        self.freq_title.title = f"Frequency: {slider_to_freq(self.freq_slider.value)}"
        self.pref['frequency'] = slider_to_freq(self.freq_slider.value)

        if self.osc.stream is not None:
            self.osc.stop()
            self.osc.play(
                wave_type=self.pref['wave_type'],
                amplitude=self.pref['amplitude'],
                frequency=self.pref['frequency'])


    def check_updates(self, sender):
        """ edit oscillator settings """
        win = rumps.Window(title=self.config["pref"], ok='Done')
        win.icon = 'icon.icns'
        win.add_buttons('Sine', 'Square', 'White Noise', 'Pink Noise')
        win.run()

    def run(self):
        """ run the app """
        self.app.run()


# ---------------------------------- Run Time ----------------------------------

if __name__ == '__main__':
    app = BarOscApp()
    app.run()
