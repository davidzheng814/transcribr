import midi
import random
from os.path import *

DURATION_RANGE = (150, 250)
VOLUME_RANGE = (100, 150)
PITCH_RANGE = (60, 80)
NUM_TICKS = 20000
RESOLUTION = 220
TEMPO = 250
SAMPLE_RATE = 20
TICKS_PER_WINDOW = TEMPO * RESOLUTION / (SAMPLE_RATE * 60)

MIDI_DIR = './midi_samples'
FILENAME_BASE = 'sample'
NUM_SAMPLES = 200

def generate_random_midi():
    pattern = midi.Pattern(resolution=220)
    track = midi.Track()
    pattern.append(track)

    ticks = 0
    tick_buffer = 0
    pitches = []
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
            pitches.append(pitch - 9)

        on = midi.NoteOnEvent(tick=0, velocity=volume, pitch=pitch)
        off = midi.NoteOffEvent(tick=duration, pitch=pitch)
        track.extend([on, off])

    eot = midi.EndOfTrackEvent(tick=1)
    track.append(eot)

    return pattern

if __name__ == '__main__':
    for i in range(NUM_SAMPLES):
        filename = join(MIDI_DIR, FILENAME_BASE+"_"+str(i)+".mid")
        midi.write_midifile(filename, generate_random_midi())