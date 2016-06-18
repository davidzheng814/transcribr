import sys
import midi
import random
import numpy as np
from os.path import *

DURATION_RANGE = (170, 290)
VOLUME_RANGE = (90, 110)
PITCH_RANGE = (60, 80)
MAX_PITCH_VALUE = 128
NUM_TICKS = 20000
RESOLUTION = 220
TEMPO = 130
SAMPLE_RATE = 20
TICKS_PER_WINDOW = TEMPO * RESOLUTION / (SAMPLE_RATE * 60)
NEURAL_NET_DELAY = 5 #in windows

OUTPUT_FILE = 'training_data_outputs.npz'
MIDI_DIR = './midi_samples'
FILENAME_BASE = 'sample'
NUM_SAMPLES = 200

def generate_random_midi():
    pattern = midi.Pattern(resolution=220)
    track = midi.Track()
    pattern.append(track)

    ticks = 0
    tick_buffer = 0
    pitches = [-1] * NEURAL_NET_DELAY #use -1 to indicate a rest
    set_tempo = midi.SetTempoEvent()
    set_tempo.set_bpm(TEMPO)
    track.append(set_tempo)
    while ticks < NUM_TICKS:
        duration = random.randint(*DURATION_RANGE)
        volume = random.randint(*VOLUME_RANGE)
        pitch = random.randint(*PITCH_RANGE)
        if duration + ticks > NUM_TICKS:
            duration = NUM_TICKS - ticks

        ticks += duration
        tick_buffer += duration

        while tick_buffer > 0:
            tick_buffer -= TICKS_PER_WINDOW
            pitches.append(pitch - PITCH_RANGE[0])

        on = midi.NoteOnEvent(tick=0, velocity=volume, pitch=pitch)
        off = midi.NoteOffEvent(tick=duration, pitch=pitch)
        track.extend([on, off])

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)

    return (pattern, pitches)

def generate_numpy_array(pitches):
    pitch_array = np.zeros((len(pitches), PITCH_RANGE[1] - PITCH_RANGE[0] +1))
    for i in range(len(pitches)):
        pitch_value = pitches[i]
        if pitch_value >= 0:
            pitch_array[i][pitch_value] = 1
    return pitch_array

if __name__ == '__main__':

    output_file = OUTPUT_FILE
    if len(sys.argv) > 1:
        output_file = sys.argv[-1]
    pitch_array_dict = {}

    for i in range(NUM_SAMPLES):
        basename = FILENAME_BASE+"_"+str(i)
        print "working on file " + basename
        filename = join(MIDI_DIR, basename+".mid")
        pattern, pitches = generate_random_midi()
        pitch_array_dict[basename] = generate_numpy_array(pitches)
        midi.write_midifile(filename, pattern)

    np.savez_compressed(output_file, **pitch_array_dict)