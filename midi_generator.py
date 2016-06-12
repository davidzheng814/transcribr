import midi
import random
from os.path import *

DURATION_RANGE = (150, 250)
VOLUME_RANGE = (100, 150)
PITCH_RANGE = (60, 80)
NUM_TICKS = 20000

DIR = './midi_samples'
FILENAME_BASE = 'sample'
NUM_SAMPLES = 200

def generate_random_midi():
    pattern = midi.Pattern()
    track = midi.Track()
    pattern.append(track)

    ticks = 0
    while ticks < NUM_TICKS:
        duration = random.randint(*DURATION_RANGE)
        volume = random.randint(*VOLUME_RANGE)
        pitch = random.randint(*PITCH_RANGE)
        if duration + ticks > NUM_TICKS:
            duration = NUM_TICKS - ticks

        ticks += duration
        
        on = midi.NoteOnEvent(tick=0, velocity=volume, pitch=pitch)
        off = midi.NoteOffEvent(tick=duration, pitch=pitch)
        track.extend([on, off])

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)

    return pattern

if __name__ == '__main__':
    for i in range(NUM_SAMPLES):
        filename = join(DIR, FILENAME_BASE+"_"+str(i)+".mid")
        midi.write_midifile(filename, generate_random_midi())