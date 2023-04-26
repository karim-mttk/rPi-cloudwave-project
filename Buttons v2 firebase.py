
import RPi.GPIO as GPIO
import time
import pygame

import firebase_admin
from firebase_admin import credentials, storage, db

# pygame setup
pygame.mixer.init()

# firebase setup
cred = credentials.Certificate(r"firebasekey.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'cloudwave-test.appspot.com', 'databaseURL': 'https://cloudwave-test-default-rtdb.europe-west1.firebasedatabase.app'})

# create a Firebase Storage client
bucket = storage.bucket()
root = db.reference("/")

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

# function to redefine index from firebase in main loop later


def Check_index():
    return root.child('index').get()


chord_index = Check_index()

# selecting chords
Chords = [{"note": "C"}, {"note": "D"}, {"note": "E"}, {"note": "F"},
          {"note": "G"}, {"note": "A"}, {"note": "B"}, {"note": "C#"},
          {"note": "D#"}, {"note": "F#"}, {"note": "G#"}, {"note": "A#"}]

# function to redefine chords from firebase in main loop later
# download all chords and put in local storage


def Download_Chords(index):
    FXBoard = []
    for note in Chords:
        # specify the path to the audio file in Firebase Storage
        storage_path = rf"sounds{index}/folder/{note['note']}.wav"

        # download the sound file to a temporary file
        temp_file = rf"/home/pi/Desktop/programming/cloudwave/sound/{note['note']}.wav"
        blob = bucket.blob(storage_path)
        blob.download_to_filename(temp_file)

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        print(f"finished downloading {note['note']}.wav")
    return FXBoard


SoundBoard = Download_Chords(chord_index)

try:
    while True:
        # change soundboard if index differ
        if chord_index != Check_index():
            chord_index = Check_index()
            SoundBoard = Download_Chords(chord_index)

        # if button pressed, play sound
        if GPIO.input(4) == 0:
            print("Sound C")      # play sound
            SoundBoard[0].play()                # plays sound at index
            time.sleep(0.25)
        if GPIO.input(27) == 0:
            print("Sound D")      # play sound
            SoundBoard[1].play()   # plays sound at index
            time.sleep(0.25)
        if GPIO.input(22) == 0:
            print("Sound E")      # play sound
            SoundBoard[2].play()   # plays sound at index
            time.sleep(0.25)
        if GPIO.input(5) == 0:
            print("Sound F")  # play sound
            SoundBoard[3].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(6) == 0:
            print("Sound G")      # play sound
            SoundBoard[4].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(26) == 0:
            print("Sound A")      # play sound
            SoundBoard[5].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(23) == 0:
            print("Sound B")      # play sound
            SoundBoard[6].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(25) == 0:
            print("Sound C# ")      # play sound
            SoundBoard[7].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(2) == 0:
            print("Sound D#")      # play sound
            SoundBoard[8].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(3) == 0:
            print("Sound F#")      # play sound
            SoundBoard[9].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(24) == 0:
            print("Sound G#")      # play sound
            SoundBoard[10].play()  # plays sound at index
            time.sleep(0.25)
        if GPIO.input(8) == 0:
            print("Sound A#")      # play sound
            SoundBoard[11].play()  # plays sound at index
            time.sleep(0.25)
except KeyboardInterrupt:
    pygame.mixer.stop()
    GPIO.cleanup()


