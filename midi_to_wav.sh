for var in midi_samples/*
do 
    timidity $var -Ow
done

mv midi_samples/*.wav wav_samples/
