
import RPi.GPIO as GPIO
import time
import pygame

import firebase_admin
from firebase_admin import credentials, storage

# pygame setup
pygame.mixer.init()


# firebase setup
cred = credentials.Certificate(r"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\firebase key\cloudwave-test-firebase-adminsdk-ejn2w-6a4e295421.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'cloudwave-test.appspot.com'
})

# create a Firebase Storage client
bucket = storage.bucket()

# GPIO setup
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
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # G# GPIO 7
GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # A# GPIO 8

# download index number
index_path = 'index.txt'
# change to RPi storage path later
index_temp_file = r'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp/index.txt'

# function to redefine index in main loop later
def Check_index():
    blob = bucket.blob(index_path)
    blob.download_to_filename(index_temp_file)
    with open(index_temp_file) as file:
        return int(file.read())


chord_index = Check_index()

# selecting chords
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

# function to redefine chords in main loop later
# download all chords and put in local storage
def Download_Chords(index):
    FXBoard = {}
    IndexPath = 0
    for note in Chords:
        # specify the path to the audio file in Firebase Storage
        storage_path = rf"sounds{index}/folder/{note['note']}.mp3"

        # download the sound file to a temporary file
        # change to RPi storage path later
        temp_file = rf"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp/{note['note']}.mp3"
        blob = bucket.blob(storage_path)
        blob.download_to_filename(temp_file)

        # load the sound file into Pygame mixer and save it
        FXBoard[IndexPath] = pygame.mixer.Sound(temp_file)
        IndexPath += 1
    return FXBoard


SoundBoard = Download_Chords(chord_index)

index = 0
try:
    while True:
        # change soundboard if index differ
        if chord_index != Check_index():
            chord_index = Check_index
            SoundBoard = Download_Chords(chord_index)
        if GPIO.input(4) == 0:
            print("Sound C")      # play sound
            SoundBoard[index].play()                # plays sound at index
            time.sleep(0.25)
        if GPIO.input(27) == 0:
            print("Sound D")      # play sound
            SoundBoard[index].play()   # plays sound at index
            time.sleep(0.25)
        if GPIO.input(22) == 0:
            print("Sound E")      # play sound
            SoundBoard[index].play()   # plays sound at index
            time.sleep(0.25)
        if GPIO.input(5) == 0:
            print("Sound F")  # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(6) == 0:
            print("Sound G")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(26) == 0:
            print("Sound A")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(23) == 0:
            print("Sound B")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(25) == 0:
            print("Sound C# ")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(2) == 0:
            print("Sound D#")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(3) == 0:
            print("Sound F#")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(24) == 0:
            print("Sound G#")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(8) == 0:
            print("Sound A#")      # play sound
            SoundBoard[index].play()  # plays sound at index
            time.sleep(0.25)
except KeyboardInterrupt:
    mixer.stop()
    GPIO.cleanup()


