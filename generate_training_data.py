import sys
import wave
import numpy as np

def generate_training_data(filename):
    wav = wave.open(filename, 'r')
    params = wav.getparams()
    nchannels, width, framerate, nframes = params[:4]
    sample = wav.readframes(nframes)
    if nchannels == 2 and width == 2:
        data = np.array([(ord(sample[i]) << 8) + ord(sample[i+1]) for i in range(0,len(sample),2)])
        data = data[0::2]
    else:
        raise "Incompatible WAV File"
        
    wav.close()

if __name__ == '__main__':
    output_dir = sys.argv[-1]
    for filename in sys.argv[1:-1]:
        generate_training_data(filename)