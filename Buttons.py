
import RPi.GPIO as GPIO
import time
import pygame
from pygame import mixer

mixer.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# defining pins and GPIO mode
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # C GPIO 4         pin 17 kanske
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # D GPIO 27
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # E GPIO 22
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # F GPIO 5
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # G GPIO 6
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # A GPIO 26
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # B GPIO 23
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # C# GPIO 25
GPIO.setup(2, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # D# GPIO 2
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # F# GPIO 3
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # G# GPIO 7
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # A# GPIO 8

# alternative method for selecting files
Chords = [{"note": "C"},
          {"note": "D"},
          {"note": "E"},
          {"note": "F"},
          {"note": "G"},
          {"note": "A"},
          {"note": "B"},
          {"note": "C#"},
          {"note": "D#"},
          {"note": "F#"},
          {"note": "G#"},
          {"note": "A#"}]

# Load chord sound files
FXBoard = {}
index = 0
for note in Chords:
    sound = pygame.mixer.Sound(f"{note['note']}.wav")   # signed 16 bit Little Endian Rate 22050 Hz, mono
    FXBoard[index] = sound
    index += 1

# different chords as arrays. Store different versions of the chords here
C_chord = [pygame.mixer.Sound('C.wav')]
D_chord = [pygame.mixer.Sound('D.wav')]
E_chord = [pygame.mixer.Sound('E.wav')]
F_chord = [pygame.mixer.Sound('F.wav')]
G_chord = [pygame.mixer.Sound('G.wav')]
A_chord = [pygame.mixer.Sound('A.wav')]
B_chord = [pygame.mixer.Sound('B.wav')]
CS_chord = [pygame.mixer.Sound('C#.wav')]
DS_chord = [pygame.mixer.Sound('D#.wav')]
FS_chord = [pygame.mixer.Sound('F#.wav')]
GS_chord = [pygame.mixer.Sound('G#.wav')]
AS_chord = [pygame.mixer.Sound('A#.wav')]

# idea: have a stored file.txt where names of the files are stored.
# when initiating the program, these filenames are read, and put into the sound arrays

# arrays of sound objects, ex.
# Piano = [C_chord, D_chord, E_chord, F_chord, G_chord, A_chord,
# B_chord, CS_chord, DS_chord, FS_chord, GS_chord, AS_chord]
# Guitar = [C_chord, D_chord, E_chord, ...]

# collection of sound chord packets ex. [0] = Piano
# old SoundBoard = [Piano, Guitar]
SoundBoard = [C_chord, D_chord, E_chord, F_chord, G_chord, A_chord, B_chord,
              CS_chord, DS_chord, FS_chord, GS_chord, AS_chord]

# example with 8 custom sound packets
# SoundBoard = [Custom1, Custom2, Custom3, Custom4, Custom5, Custom6, Custom7, Custom8]

# sound board array index
index = 0
try:
    while True:
        # sudo code:
        # if variable_for_sound_change == 1 and index < len(SoundBoard) - 1:
        #   index = 1
        # elif variable_for_sound_change == 1 and index >= len(SoundBoard) - 1:
        #   index = 0
        if GPIO.input(17) == 0:
            print("Sound C")      # play sound
            SoundBoard[0][index].play()                # plays sound at index
            time.sleep(0.25)
        if GPIO.input(13) == 0:
            print("Sound D")      # play sound
            SoundBoard[1][index].play()   # plays sound at index
            time.sleep(0.25)
        if GPIO.input(15) == 0:
            print("Sound E")      # play sound
            SoundBoard[2][index].play()   # plays sound at index
            time.sleep(0.25)
        if GPIO.input(29) == 0:
            print("Sound F")  # play sound
            SoundBoard[3][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(31) == 0:
            print("Sound G")      # play sound
            SoundBoard[4][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(37) == 0:
            print("Sound A")      # play sound
            SoundBoard[5][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(24) == 0:
            print("Sound B")      # play sound
            SoundBoard[6][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(22) == 0:
            print("Sound C# ")      # play sound
            SoundBoard[7][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(3) == 0:
            print("Sound D#")      # play sound
            SoundBoard[8][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(5) == 0:
            print("Sound F#")      # play sound
            SoundBoard[9][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(26) == 0:
            print("Sound G#")      # play sound
            SoundBoard[10][index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(24) == 0:
            print("Sound A#")      # play sound
            SoundBoard[11][index].play()  # plays sound at index
            time.sleep(0.25)
except KeyboardInterrupt:
    mixer.stop()
    GPIO.cleanup()


