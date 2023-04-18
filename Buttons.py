
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(7, GPIO.IN)  # C GPIO 4
GPIO.setup(13, GPIO.IN)  # D GPIO 27
GPIO.setup(15, GPIO.IN)  # E GPIO 22
GPIO.setup(29, GPIO.IN)  # F GPIO 5
GPIO.setup(31, GPIO.IN)  # G GPIO 6
GPIO.setup(37, GPIO.IN)  # A GPIO 26
GPIO.setup(16, GPIO.IN)  # B GPIO 23
GPIO.setup(22, GPIO.IN)  # C# GPIO 25
GPIO.setup(3, GPIO.IN)  # D# GPIO 2
GPIO.setup(5, GPIO.IN)  # F# GPIO 3
GPIO.setup(26, GPIO.IN)  # G# GPIO 7
GPIO.setup(24, GPIO.IN)  # A# GPIO 8

while True:
    if GPIO.input(2) == 0:
        print("Sound")      # play sound
        time.sleep(0.25)
