
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN)  # C
GPIO.setup(4, GPIO.IN)  # D
GPIO.setup(4, GPIO.IN)  # E
GPIO.setup(4, GPIO.IN)  # F
GPIO.setup(4, GPIO.IN)  # G
GPIO.setup(4, GPIO.IN)  # A
GPIO.setup(4, GPIO.IN)  # B
GPIO.setup(4, GPIO.IN)  # C#
GPIO.setup(4, GPIO.IN)  # D#
GPIO.setup(4, GPIO.IN)  # F#
GPIO.setup(4, GPIO.IN)  # G#
GPIO.setup(4, GPIO.IN)  # A#

while True:
    if GPIO.input(2) == 0:
        print("Hello")      # play sound
        time.sleep(0.25)