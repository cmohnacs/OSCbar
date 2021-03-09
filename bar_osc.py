"""
Bar Osc App

Calibration oscillator for the macOS menu bar
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

def freq_title_format(frequency):
    """ Frequency: 440 """
    return f"Frequency: {frequency}"


# -------------------------------- Menu Bar App --------------------------------

class BarOscApp:
    """ Bar Osc object """

    def __init__(self):
        self.samplerate = 44100
        self.wave_type = "sine_wave"
        self.amplitude = 0.5
        self.frequency = 440
        self.app = rumps.App("Bar Osc")
        # set up menu
        self.build_menu()
        self.ready_menu()
        # single oscillator instance for the app
        self.osc = Oscillator( self.samplerate,
                                self.wave_type,
                                self.amplitude,
                                self.frequency)

    def build_menu(self):
        """ define menu, buttons, sliders """
        # menu items
        self.start_button = rumps.MenuItem(                 # Start Osc
            title="Start Oscillator")
        self.stop_button = rumps.MenuItem(                  # Stop Osc
            title="Stop Oscillator")
        self.amp_title = rumps.MenuItem(                   # Volume title
            title="Volume",
            callback=None)
        self.amp_slider = rumps.SliderMenuItem(            # Volume slider
            value=self.amplitude,
            min_value=0.0,
            max_value=1.0,
            callback=self.adj_amp,
            dimensions=(180, 20))
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
            title=freq_title_format(self.frequency),
            callback=None)
        self.freq_slider = rumps.SliderMenuItem(            # Frequency slider
            value=freq_to_slider(self.frequency),
            min_value=freq_to_slider(20),                   # 20Hz - 20kHz
            max_value=freq_to_slider(20000),
            callback=self.adj_freq,
            dimensions=(180, 20))
        self.check_updates_button = rumps.MenuItem(         # Check for updates
            title="Check for updates...",
            callback=None)
        #populate menu
        self.app.menu =    [self.start_button,
                            self.stop_button,
                            None,
                            self.amp_title,
                            self.amp_slider,
                            None,
                            self.sine_button,
                            self.square_button,
                            self.white_noise_button,
                            None,
                            self.freq_title,
                            self.freq_slider,
                            None,
                            self.check_updates_button]

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
        """ Start Oscillator callback """
        # update menu and title
        self.busy_menu()
        # generate osc tone
        self.osc.play()

    def stop_osc(self, sender):
        """ Stop Oscillator callback """
        # update menu and title
        self.ready_menu()
        # kill osc tone
        self.osc.stop()

    def set_sine_wave(self, sender):
        """ Sine Wave callback """
        self.sine_button.set_callback(None)
        self.square_button.set_callback(self.set_square_wave)
        self.white_noise_button.set_callback(self.set_white_noise)

        self.wave_type = 'sine_wave'
        self.osc.set_wave_type('sine_wave')

    def set_square_wave(self, sender):
        """ Square Wave callback """
        self.sine_button.set_callback(self.set_sine_wave)
        self.square_button.set_callback(None)
        self.white_noise_button.set_callback(self.set_white_noise)

        self.wave_type = 'square_wave'
        self.osc.set_wave_type('square_wave')

    def set_white_noise(self, sender):
        """ White Noise callback """
        self.sine_button.set_callback(self.set_sine_wave)
        self.square_button.set_callback(self.set_square_wave)
        self.white_noise_button.set_callback(None)

        self.wave_type = 'white_noise'
        self.osc.set_wave_type('white_noise')

    def adj_freq(self, sender):
        """ Frequency slider callback """
        # when slider adjusted, update title and osc freq
        self.frequency = slider_to_freq(self.freq_slider.value)
        self.freq_title.title = freq_title_format(self.frequency)
        self.osc.set_frequency(self.frequency)

    def adj_amp(self, sender):
        """ Amplitude slider callback """
        self.amplitude = self.amp_slider.value
        self.osc.set_amplitude(self.amplitude)

    def check_updates(self, sender):
        """ Check for updates... callback """
        pass

    def run(self):
        """ run it """
        self.app.run()


# ---------------------------------- Run Time ----------------------------------

if __name__ == '__main__':
    app = BarOscApp()
    app.run()
