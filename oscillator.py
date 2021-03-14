""" Oscillator for Bar Osc App """

import sys
import numpy as np

import sounddevice as sd
from numpy.fft import rfft, irfft


# ------------------------------ Helper Functions ------------------------------

def amplitude_limit(amplitude):
    """
    amplitude should have min/max (0.0-1.0) to avoid clipping waveforms
    """
    if amplitude > 1.0:
        amplitude = 1.0
    elif amplitude < 0.0:
        amplitude = 0.0
    return amplitude


# ------------------------------ Wave Generators -------------------------------

def wave_generator(sample_block, wave_type='sine_wave', amplitude=0.5, frequency=440):
    """
    Wave type selector
    Default oscillator values
    """
    wave_generators = { 'sine_wave':   sine_wave,
                        'square_wave': square_wave,
                        'white_noise': white_noise,
                        'pink_noise':  pink_noise }

    return wave_generators[wave_type](sample_block, amplitude, frequency)

def sine_wave(sample_block, amplitude, frequency):
    """
    generate sine wave samples

    amplitude = volume
    frequency = Hz
    """
    return amplitude * np.sin(2 * np.pi * frequency * sample_block)

def square_wave(sample_block, amplitude, frequency):
    """
    generate square wave samples

    amplitude = volume
    frequency = Hz
    """
    wave_block = sine_wave(sample_block, amplitude, frequency)
    wave_block[wave_block > 0] = amplitude
    wave_block[wave_block < 0] = -amplitude
    return wave_block

def white_noise(sample_block, amplitude, frequency):
    """
    generate white noise samples

    amplitude = volume
    frequency N/A
    """
    return amplitude * np.random.uniform(-1, 1, sample_block.size)

def pink_noise(sample_block, amplitude, frequency):
    """
    generate pink noise samples using (real) fast fourier transform

    amplitude = volume
    frequency N/A
    """
    wave_block = white_noise(sample_block, amplitude, frequency)
    X = rfft(wave_block)
    S = np.sqrt(np.arange(X.size)+1.)
    Y = irfft(X/S, wave_block.size)
    return Y


# --------------------------------- Oscillator ---------------------------------

class Oscillator:
    """ Oscillator """

    def __init__(self, samplerate, wave_type, amplitude, frequency):
        self.stream = None
        self.samplerate = samplerate
        self.wave_type = wave_type
        self.amplitude = amplitude_limit(amplitude)
        self.frequency = frequency

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
            #print('OSCILLATOR ===>', self.wave_type, self.amplitude, self.frequency)
            data = wave_generator(sample_block,
                                        self.wave_type,
                                        self.amplitude,
                                        self.frequency)
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
    SR = 44100
    AMP = 0.2
    FREQ = 440

    osc = Oscillator(   samplerate=SR,
                        wave_type='sine_wave',
                        amplitude=AMP,
                        frequency=FREQ)
    osc.play()
    time.sleep(0.5)
    osc.stop()

    osc = Oscillator(   samplerate=SR,
                        wave_type='square_wave',
                        amplitude=AMP,
                        frequency=FREQ)
    osc.play()
    time.sleep(0.5)
    osc.stop()

    osc = Oscillator(   samplerate=SR,
                        wave_type='white_noise',
                        amplitude=AMP,
                        frequency=FREQ)
    osc.play()
    time.sleep(0.5)
    osc.stop()

    osc = Oscillator(   samplerate=SR,
                        wave_type='pink_noise',
                        amplitude=AMP,
                        frequency=FREQ)
    osc.play()
    time.sleep(0.5)
    osc.stop()
