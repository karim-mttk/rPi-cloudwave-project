import RPi.GPIO as GPIO
import alsaaudio

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

# Set up ALSA mixer
mixer = alsaaudio.Mixer(control='Headphone', cardindex=2)

# Define callback function to adjust volume
def change_volume(channel):
    volume = alsaaudio.Mixer(control='Headphone', cardindex=2).getvolume()[0]
    if channel == 27 and volume < 100:
        mixer.setvolume(volume+1)

# Add event detection to GPIO
GPIO.add_event_detect(27, GPIO.RISING, callback=change_volume)

# Keep script running
while True:
    pass
