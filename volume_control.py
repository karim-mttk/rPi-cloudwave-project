import RPi.GPIO as GPIO
import alsaaudio

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(14, GPIO.IN)
GPIO.setup(15, GPIO.IN)

# Set up ALSA mixer
mixer = alsaaudio.Mixer(control='Headphone', id=0)

# Define callback function to adjust volume
def change_volume(channel):
    volume = mixer.getvolume()[0]
    if channel == 14 and volume < 90:
        mixer.setvolume(volume + 5)
    elif channel == 15 and volume > 10:
        mixer.setvolume(volume - 5)

# Add event detection to GPIOs
GPIO.add_event_detect(14, GPIO.RISING, callback=change_volume)
GPIO.add_event_detect(15, GPIO.RISING, callback=change_volume)
# Keep script running
while True:
    pass
