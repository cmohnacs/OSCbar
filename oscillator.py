""" Oscillator for Bar Osc App """

import sys
import random
import numpy as np
import sounddevice as sd


# ------------------------------ Helper Functions ------------------------------

def amplitude_scale(amplitude):
    """ amplitude should have min of 0.0, max of 1.0 """
    if amplitude > 1.0:
        amplitude = 1.0
    elif amplitude < 0.0:
        amplitude = 0.0
    return amplitude


# ------------------------------ Wave Generators -------------------------------

def wave_generator(sample_block, wave_type='sine_wave', amplitude=0.5, frequency=440):
    """ wave type selector """
    if wave_type == 'sine_wave':
        return sine_wave(sample_block, amplitude, frequency)
    if wave_type == 'square_wave':
        return square_wave(sample_block, amplitude, frequency)
    if wave_type == 'white_noise':
        return white_noise(sample_block, amplitude)

def sine_wave(sample_block, amplitude, frequency):
    """
    calculate sine wave samples

    amplitude = volume
    frequency = Hz
    """
    return amplitude * np.sin(2 * np.pi * frequency * sample_block)

def square_wave(sample_block, amplitude, frequency):
    """
    calculate square wave samples

    amplitude = volume
    frequency = Hz
    """
    wave_block = sine_wave(sample_block, amplitude, frequency)
    for sample in wave_block:
        if sample[0] > 0:
            sample[0] = amplitude
        if sample[0] < 0:
            sample[0] = -amplitude
    return wave_block


def white_noise(sample_block, amplitude):
    """
    calculate white noise samples

    amplitude = volume
    frequency = Hz
    """
    for sample in sample_block:
        sample[0] = amplitude * random.uniform(-1, 1)
    return sample_block


# --------------------------------- Oscillator ---------------------------------

class Oscillator:
    """ Oscillator """

    def __init__(self, samplerate, wave_type, amplitude, frequency):
        self.stream = None
        self.samplerate = samplerate
        self.wave_type = wave_type
        self.amplitude = amplitude_scale(amplitude)
        self.frequency = frequency

    def set_wave_type(self, wave_type):
        self.wave_type = wave_type

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    def set_frequency(self, frequency):
        self.frequency = frequency

    def play(self): #, wave_type, amplitude, frequency
        """ stream to output """

        #amplitude = amplitude_scale(self.amplitude)

        start_idx = 0

        def callback(outdata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            # 1-D ndarray of arrays, block of samples to be calculated
            nonlocal start_idx
            sample_block = (start_idx + np.arange(frames)) / self.samplerate
            sample_block = sample_block.reshape(-1, 1)
            # calculate waveform for given samples
            outdata[:] = wave_generator(sample_block,
                                        self.wave_type,
                                        self.amplitude,
                                        self.frequency)
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

    # beep
    osc = Oscillator(samplerate=44100, wave_type='sine_wave',
                     amplitude=0.5, frequency=440)
    #HZ = 440
    #osc.play(wave_type='sine_wave', amplitude=0.5, frequency=HZ)
    osc.play()
    time.sleep(1)
    osc.stop()
