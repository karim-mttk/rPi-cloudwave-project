from pydub import AudioSegment

# Load the audio file
sound = AudioSegment.from_file("clap.wav", format="wav")

# Define the gain adjustments in decibels
bass_gain = 3
volume_gain = -2
mid_gain = 1
treble_gain = -3

# Apply the gain adjustments to the audio
adjusted_sound = sound \
    .low_pass_filter(bass_gain) \
    .high_pass_filter(treble_gain) \
    .apply_gain(volume_gain) \
    .apply_gain_stereo(mid_gain, 1)

# Play back the adjusted sound
adjusted_sound.export("output_file.wav", format="wav")


