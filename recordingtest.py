import RPi.GPIO as GPIO
import alsaaudio
import wave

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

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

# Define function to start recording
def start_recording(channel):
    print('Recording started')
    with alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, cardindex=2) as capture:
        capture.setchannels(CHANNELS)
        capture.setrate(RATE)
        capture.setformat(FORMAT)
        capture.setperiodsize(CHUNK_SIZE)
        while GPIO.input(channel):
            l, data = capture.read()
            if l:
                wave_file.writeframes(data)

# Define function to stop recording
def stop_recording(channel):
    print('Recording stopped')
    wave_file.close()

# Add event detection to GPIO
GPIO.add_event_detect(17, GPIO.RISING, callback=start_recording)
GPIO.add_event_detect(17, GPIO.FALLING, callback=stop_recording)

# Keep script running
while True:
    pass
