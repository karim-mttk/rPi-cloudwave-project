
import RPi.GPIO as GPIO
import time
import pygame
import numpy as np
import soundcard as sc
from scipy.io.wavfile import write
import pyttsx3
from eq_test import equalizerSet

import firebase_admin
from firebase_admin import credentials, storage, db

# pygame setup
pygame.init()
pygame.mixer.init(frequency=44100, size=16, channels=2, buffer=4096)

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
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # C GPIO 4
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

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # universal knapp
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # potentiometer


# function to redefine index from firebase in main loop later
macAdress = "dc:a6:32:b4:da:a5"


# read text

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# add new button, "universal knapp". To end typen password, for example


def type_synth_password():
    Password = ""
    while True:
        if GPIO.input(4) == 0:
            print("Sound C")
            Password += "C"
            time.sleep(0.25)
        if GPIO.input(27) == 0:
            print("Sound D")
            Password += "D"
            time.sleep(0.25)
        if GPIO.input(22) == 0:
            print("Sound E")
            Password += "E"
            time.sleep(0.25)
        if GPIO.input(5) == 0:
            print("Sound F")
            Password += "F"
            time.sleep(0.25)
        if GPIO.input(6) == 0:
            print("Sound G")
            Password += "G"
            time.sleep(0.25)
        if GPIO.input(26) == 0:
            print("Sound A")
            Password += "A"
            time.sleep(0.25)
        if GPIO.input(23) == 0:
            print("Sound B")
            Password += "B"
            time.sleep(0.25)
        if GPIO.input(25) == 0:
            print("Sound C# ")
            Password += "C#"
            time.sleep(0.25)
        if GPIO.input(2) == 0:
            print("Sound D#")
            Password += "D#"
            time.sleep(0.25)
        if GPIO.input(3) == 0:
            print("Sound F#")
            Password += "F#"
            time.sleep(0.25)
        if GPIO.input(24) == 0:
            print("Sound G#")
            Password += "G#"
            time.sleep(0.25)
        if GPIO.input(8) == 0:
            print("Sound A#")
            Password += "A#"
            time.sleep(0.25)
        if GPIO.input(17) == 0:     # stop typing password
            return Password


def validate_synth_password():
    while True:
        try:
            # find device, find current user, and find current user password
            Device = root.child(f'{macAdress}')
            CurrentUser = Device.child('CurrentUser').child('User').get()
            User = Device.child('users').child(f'{CurrentUser}')
            User_password = User.child('synthPassword').get()

            print("Type password:")
            speak("Type password")
            Input_password = type_synth_password()
            if Input_password == User_password:
                break
            else:
                print("Wrong password")
                speak("Wrong password")
        except:
            print("Exception, user not found")
            speak("Exception, user not found")
    return CurrentUser


current_user = validate_synth_password()

# download index number


def Check_index():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('index').get()

def Check_bass():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('Bass').get()

def Check_mid():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('Mid').get()

def Check_treble():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('Treble').get()


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
        # storage_path = rf"sounds{index}/folder/{note['note']}.wav"
        storage_path = rf"{current_user}/sounds{index}/{note['note']}.wav"

        # download the sound file to a temporary file
        temp_file = rf"/home/pi/Desktop/programming/cloudwave/sound/{note['note']}.wav"
        blob = bucket.blob(storage_path)
        blob.download_to_filename(temp_file)

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        print(f"finished downloading {note['note']}.wav")
    return FXBoard


SoundBoard = Download_Chords(chord_index)

# init recording
#

# get a list of all microphones:v
mics = sc.all_microphones(include_loopback=True)

# get the current default microphone on your system:
default_mic = mics[1]

# play all sounds, wait for each sound to finish playing
start_time = pygame.time.get_ticks()

is_recording = False

with default_mic.recorder(samplerate=44100) as mic:
    frames = []
    num_frames = 44100 * 0.5  # record for 5 seconds
    data = 0


def save_and_upload(song):
    path = fr'/home/pi/Desktop/programming/cloudwave/sound/new_song.wav'
    frames = np.concatenate(song)
    frames /= 1.414
    frames *= 32767
    uint16_data = frames.astype(np.int16)
    write(path, 44100, uint16_data)

    # upload to firebase
    upload_path = rf"{current_user}/Saved_Music/new_song.wav"
    blob = bucket.blob(upload_path)
    blob.upload_from_filename(path)

    print(f"finished uploading new_song.wav")


# check and update equalizer
# equalizerSet(Check_bass(), Check_treble(), Check_mid())

try:
    while True:
        # recording music and uploading
        if GPIO.input(17) == 0 and is_recording is False:
            speak("Recording in progress")
            is_recording = True
        elif GPIO.input(17) == 0 and is_recording is True:
            save_and_upload(frames)
            speak("Recording stopped")
            is_recording = False
        if is_recording is True:
            data = default_mic.record(numframes=num_frames, samplerate=44100)
            frames.append(data)

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


