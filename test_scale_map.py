import numpy as np

# E Minor scale semitone indices: (E is root = 4)
# Major scale: [0, 2, 4, 5, 7, 9, 11]
# Natural Minor (from E): E(4), F#(6), G(7), A(9), B(11), C(0), D(2)
em_scale = {4, 6, 7, 9, 11, 0, 2}

def nearest_scale_midi(midi_pitch):
    # Find nearest midi note that belongs to em_scale
    rounded = int(round(midi_pitch))
    if (rounded % 12) in em_scale:
        return float(rounded)
    # Check +1 and -1
    up = rounded + 1
    down = rounded - 1
    if (up % 12) in em_scale:
        return float(up)
    if (down % 12) in em_scale:
        return float(down)
    return float(rounded)

print("E Minor scale test:")
for m in [63, 64, 65, 66, 67, 68, 69]: # D#4, E4, F4, F#4, G4, G#4, A4
    print(f"MIDI {m} -> Nearest E Minor: {nearest_scale_midi(m)}")
