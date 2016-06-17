import sys
import wave
import numpy as np
import os.path

from scipy.fftpack import dct
from math import ceil

SAMPLING_RATE = 44100
WINDOW_SIZE = SAMPLING_RATE / 20
NUM_SAMPLES = 200
TRAINING_DATA_OUTPUT_FILE = 'training_data_outputs.npz'
TRAINING_DATA_INPUT_FILE = 'training_data_inputs.npz'
FILENAME_LIST = ['wav_samples/sample_' + str(i) + '.wav' for i in range(NUM_SAMPLES)]

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

    # for future files, might have to pad with zeros for NEURAL_NET_DELAY
    return dft_array

if __name__ == '__main__':

    training_data_outputs_file = TRAINING_DATA_OUTPUT_FILE
    output_file = TRAINING_DATA_INPUT_FILE
    filename_list = FILENAME_LIST

    if len(sys.argv) > 1:
        output_file = sys.argv[-1]
        training_data_outputs_file = sys.argv[-2]
        filename_list = sys.argv[1:-2]

    training_data_outputs = np.load(training_data_outputs_file)
    dft_dict = {}

    for filename in filename_list:
        basename = os.path.splitext(os.path.basename(filename))[0]
        print "working on file " + basename
        size = training_data_outputs[basename].shape[0]
        dft_dict[basename] = windowed_DFT(generate_training_data(filename))[:size]

    np.savez_compressed(output_file, **dft_dict)