"""
Oscillator for Oscbar App
"""

import sys
import numpy as np

import sounddevice as sd
from numpy.fft import rfft, irfft


# wave types available to oscillator, implemented in Oscillator class
WAVES =    ['sine_wave',
            'square_wave',
            'white_noise',
            'pink_noise']

def get_samplerate():
    """ get samplerate from default output """
    return sd.query_devices(kind='output')['default_samplerate']


class Oscillator:
    """ Oscillator """

    def __init__(self, wave_type, amplitude, frequency):
        self.stream = None
        self.samplerate = get_samplerate()
        self.wave_type = wave_type
        self.amplitude = amplitude
        self.frequency = frequency

    def __str__(self):
        return f"""~~~ {self.__class__.__name__.upper()} ===> SAMPLERATE: {self.samplerate},
                    WAVE: {self.wave_type},
                    AMPL: {self.amplitude},
                    FREQ: {self.frequency} Hz"""

    @property
    def wave_type(self):
        return self._wave_type

    @wave_type.setter
    def wave_type(self, wave_type):
        if wave_type not in WAVES:
            raise Exception("Wave Type is not defined")
        self._wave_type = wave_type

    @property
    def amplitude(self):
        return self._amplitude

    @amplitude.setter
    def amplitude(self, amp):
        if amp > 1.0 or amp < 0.0:
            raise Exception("Amplitude must be in range 0.0 - 1.0")
        self._amplitude = amp

    @property
    def frequency(self):
        return self._frequency

    @frequency.setter
    def frequency(self, freq):
        if freq < 20 or freq > 20000:
            raise Exception("Frequency must be in range 20 - 20000")
        self._frequency = freq

    @staticmethod
    def sine_wave(sample_block, amplitude, frequency):
        """
        generate sine wave samples

        amplitude = volume
        frequency = Hz
        """
        return amplitude * np.sin(2 * np.pi * frequency * sample_block)

    @staticmethod
    def square_wave(sample_block, amplitude, frequency):
        """
        generate square wave samples

        amplitude = volume
        frequency = Hz
        """
        wave_block = Oscillator.sine_wave(sample_block, amplitude, frequency)
        wave_block[wave_block > 0] = amplitude
        wave_block[wave_block < 0] = -amplitude
        return wave_block

    @staticmethod
    def white_noise(sample_block, amplitude, frequency):
        """
        generate white noise samples

        amplitude = volume
        frequency N/A
        """
        return amplitude * np.random.uniform(-1, 1, sample_block.size)

    @staticmethod
    def pink_noise(sample_block, amplitude, frequency):
        """
        generate pink noise samples using (real) fast fourier transform

        amplitude = volume
        frequency N/A
        """
        wave_block = Oscillator.white_noise(sample_block, amplitude, frequency)
        X = rfft(wave_block)
        S = np.sqrt(np.arange(X.size)+1.)
        Y = irfft(X/S, wave_block.size)
        return Y

    def play(self):
        """ stream to output """

        start_idx = 0

        def callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            # block of samples to be processed
            nonlocal start_idx
            sample_block = (start_idx + np.arange(frames, dtype=float)) / self.samplerate
            # calculate waveform for given samples
            try:
                data = eval("Oscillator." + self.wave_type +
                            "(sample_block, self.amplitude, self.frequency)")
            except NameError as wave_error:
                raise NotImplementedError("Wave Type not available") from wave_error
            # 2-D array with shape (_,1)
            outdata[:] = data.reshape(-1,1)
            # update index
            start_idx += frames

        # stream to output
        self.stream = sd.OutputStream(channels=1, callback=callback,
                             samplerate=self.samplerate)
        self.stream.start()


    def stop(self):
        """ stop the oscillator and close the stream """
        self.stream.stop()
        self.stream.close()


# ---------------------------------- Run Time ----------------------------------

if __name__ == '__main__':
    import time
    # beeps and noises
    AMP = 0.5
    FREQ = 440
    for wave in WAVES:
        osc = Oscillator(   wave_type=wave,
                            amplitude=AMP,
                            frequency=FREQ)
        print(osc)
        osc.play()
        time.sleep(0.5)
        osc.stop()
