
import RPi.GPIO as GPIO
import time
import pygame
from pygame import mixer

mixer.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

# defining pins and GPIO mode
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

# different chords
C_chord = pygame.mixer.Sound('C.mp3')
D_chord = pygame.mixer.Sound('D.mp3')
E_chord = pygame.mixer.Sound('E.mp3')
F_chord = pygame.mixer.Sound('F.mp3')
G_chord = pygame.mixer.Sound('G.mp3')
A_chord = pygame.mixer.Sound('A.mp3')
B_chord = pygame.mixer.Sound('B.mp3')
CS_chord = pygame.mixer.Sound('C#.mp3')
DS_chord = pygame.mixer.Sound('D#.mp3')
FS_chord = pygame.mixer.Sound('F#.mp3')
GS_chord = pygame.mixer.Sound('G#.mp3')
AS_chord = pygame.mixer.Sound('A#.mp3')

# idea: have a stored file.txt where names of the files are stored.
# when initiating the program, these filenames are read, and put into the sound arrays

# arrays of sound objects
Piano = [C_chord, D_chord, E_chord, F_chord, G_chord, A_chord, B_chord, CS_chord, DS_chord, FS_chord, GS_chord, AS_chord]           # array of sound objects
Guitar = [C_chord, D_chord, E_chord]

# collection of sound packets
SoundBoard = [Piano, Guitar]

# example with 8 custom sound packets
# SoundBoard = [Custom1, Custom2, Custom3, Custom4, Custom5, Custom6, Custom7, Custom8]

# sound board array index
index = 0

while True:
    # sudo code:
    # if variable_for_sound_change == 1 and index < len(SoundBoard) - 1:
    #   index = 1
    # elif variable_for_sound_change == 1 and index >= len(SoundBoard) - 1:
    #   index = 0
    if GPIO.input(7) == 0:
        print("Sound C")      # play sound
        SoundBoard[index][0].play()                # plays sound at index
        time.sleep(0.25)
    if GPIO.input(13) == 0:
        print("Sound D")      # play sound
        SoundBoard[index][1].play()   # plays sound at index
        time.sleep(0.25)
    if GPIO.input(15) == 0:
        print("Sound E")      # play sound
        SoundBoard[index][2].play()   # plays sound at index
        time.sleep(0.25)
    if GPIO.input(29) == 0:
        print("Sound F")  # play sound
        SoundBoard[index][3].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(31) == 0:
        print("Sound G")      # play sound
        SoundBoard[index][4].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(37) == 0:
        print("Sound A")      # play sound
        SoundBoard[index][5].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(24) == 0:
        print("Sound B")      # play sound
        SoundBoard[index][6].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(22) == 0:
        print("Sound C# ")      # play sound
        SoundBoard[index][7].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(3) == 0:
        print("Sound D#")      # play sound
        SoundBoard[index][8].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(5) == 0:
        print("Sound F#")      # play sound
        SoundBoard[index][9].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(26) == 0:
        print("Sound G#")      # play sound
        SoundBoard[index][10].play()  # plays sound at index
        time.sleep(0.25)
    if GPIO.input(24) == 0:
        print("Sound A#")      # play sound
        SoundBoard[index][11].play()  # plays sound at index
        time.sleep(0.25)

