import sys
import wave
import numpy as np
import os.path

from scipy.fftpack import dct
from math import ceil

SAMPLING_RATE = 44100
WINDOW_SIZE = SAMPLING_RATE / 20

def generate_training_data(filename):
    wav = wave.open(filename, 'r')
    params = wav.getparams()
    nchannels, width, framerate, nframes = params[:4]
    sample = wav.readframes(nframes)
    if nchannels == 2 and width == 2:
        data = np.array([(ord(sample[i]) << 8) + ord(sample[i+1]) for i in range(0,len(sample),2)])
        data = data[0::2]
        wav.close()
        return data
    else:
        raise "Incompatible WAV File"

def windowed_DFT(data):
    num_windows = int(ceil(1. * data.size / WINDOW_SIZE))
    dft_array = np.empty((num_windows, WINDOW_SIZE))

    for i in range(num_windows):
        window = data[i * WINDOW_SIZE: (i+1) * WINDOW_SIZE]
        if (window.size < WINDOW_SIZE):
            window = np.copy(window)
            window.resize(WINDOW_SIZE)
        frequencies = dct(window, type=2, norm='ortho')
        dft_array[i] = frequencies

    return dft_array

if __name__ == '__main__':
    output_dir = sys.argv[-1]
    for filename in sys.argv[1:-1]:
        basename = os.path.splitext(os.path.basename(filename))[0]
        print "working on file " + basename
        output_file = basename + '.npz'
        np.savez_compressed(os.path.join(output_dir, output_file), 
                            windowed_DFT(generate_training_data(filename)))