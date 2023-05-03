import RPi.GPIO as GPIO
import alsaaudio

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.IN)

# Set up ALSA mixer
mixer = alsaaudio.Mixer(control='Headphone', id=0)

# Define callback function to adjust volume
def change_volume(channel):
    volume = mixer.getvolume()[0]
    if volume <= 0 and channel == 27:
        mixer.setvolume(0)
    elif volume >= 100 and channel == 27:
        mixer.setvolume(100)
    elif channel == 27:
        # Read value from potentiometer (0-100) and set volume
        pot_value = GPIO.input(channel)
        volume = round(pot_value / 1023 * 100)
        mixer.setvolume(volume)

# Add event detection to GPIO
GPIO.add_event_detect(27, GPIO.BOTH, callback=change_volume)

# Keep script running
while True:
    pass
