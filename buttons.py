
import RPi.GPIO as GPIO
import time
import pygame
from pygame import mixer

mixer.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# defining pins and GPIO mode
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # C GPIO 4


# different chords
C_chord = pygame.mixer.Sound("/home/pi/Desktop/programming/cloudwae/C.mp3")
C_chord.set_volume(1)


while True:

    if GPIO.input(27) == 0:
        print("Sound C")      # play sound
        C_chord.play()                # plays sound at index
        time.sleep(0.25)
  
