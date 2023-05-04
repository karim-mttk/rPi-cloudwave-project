import RPi.GPIO as GPIO
import alsaaudio
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)

# Set up ALSA mixer
mixer = alsaaudio.Mixer(control='Headphone', id=0)

# Set up audio parameters
FORMAT = alsaaudio.PCM_FORMAT_S16_LE
CHANNELS = 2
RATE = 44100
PERIOD_SIZE = 1024

# Open audio output stream
output = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, alsaaudio.PCM_NORMAL, 'default')
output.setchannels(CHANNELS)
output.setformat(FORMAT)
output.setrate(RATE)
output.setperiodsize(PERIOD_SIZE)

# Define callback function to change pitch
def pitch_change(channel):
    pitch = alsaaudio.PCM_RATE_NEAR
    if channel == 14:
        pitch += 1000
    elif channel == 15:
        pitch -= 1000
    output.setrate(pitch)

# Add event detection to GPIOs
GPIO.add_event_detect(14, GPIO.RISING, callback=pitch_change)
GPIO.add_event_detect(15, GPIO.RISING, callback=pitch_change)

# Keep script running
while True:
    # Generate a tone and write it to the audio output stream
    tone = bytes([int(127 * math.sin(2 * math.pi * RATE * i / PERIOD_SIZE)) for i in range(PERIOD_SIZE)])
    output.write(tone)
    time.sleep(0.001)
