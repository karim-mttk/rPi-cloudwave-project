from pydub import AudioSegment
import pygame

pygame.mixer.init()

Chords = [{"note": "C"}, {"note": "D"}, {"note": "E"}, {"note": "F"},
          {"note": "G"}, {"note": "A"}, {"note": "B"}, {"note": "C#"},
          {"note": "D#"}, {"note": "F#"}, {"note": "G#"}, {"note": "A#"}]

# Define the gain adjustments in decibels


def equalizerSet(bass, mid, treble):
    # bass = 20
    # mid = 1
    # treble = 1
    equalizer = []
    for note in Chords:
        # Load the audio file
        sound = AudioSegment.from_file(rf"/home/pi/Desktop/cloudwave/sound/{note['note']}.wav", format="wav")
    
        # Apply the gain adjustments to the audio
        adjusted_sound = sound \
            .low_pass_filter(bass) \
            .high_pass_filter(treble) \
            .apply_gain(mid)
            
        # Export the adjusted sound
        adjusted_sound.export(rf"/home/pi/Desktop/cloudwave/sound/{note['note']}.wav", format="wav")
        equalizer.append(pygame.mixer.Sound(rf"/home/pi/Desktop/cloudwave/sound/{note['note']}.wav"))
    return equalizer
