import alsaaudio
import wave
import time

# Set up ALSA mixer
mixer = alsaaudio.Mixer(control='Headphone', cardindex=2)

# Set up audio parameters
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 2
RATE = 44100
CHUNK_SIZE = 1024

# Define filename and create wave file
filename = 'recording.wav'
wave_file = wave.open(filename, 'wb')
wave_file.setnchannels(CHANNELS)
wave_file.setsampwidth(2)
wave_file.setframerate(RATE)

# Start recording
print('Recording started')
with alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, cardindex=2) as capture:
    capture.setchannels(CHANNELS)
    capture.setrate(RATE)
    capture.setformat(FORMAT)
    capture.setperiodsize(CHUNK_SIZE)
    start_time = time.time()
    while time.time() - start_time < 5:
        l, data = capture.read()
        if l:
            wave_file.writeframes(data)

# Stop recording and close wave file
print('Recording stopped')
wave_file.close()
