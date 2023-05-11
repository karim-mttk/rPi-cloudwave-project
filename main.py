
import RPi.GPIO as GPIO
import time
import pygame
import wave
import numpy as np
from scipy.io.wavfile import write
import pyttsx3
from eq_test import equalizerSet
from volume_control import change_volume
from python_Scr_C_record import record


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
root = root.child('CloudWave')


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

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)       # öka volym
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)       # minska volym
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)       # octav -
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)       # octav +



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
            User_password = User.child('SynthPassword').get()

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

name = root.child(f'{macAdress}').child('users').child(f'{current_user}').child('name').get()
print(f"Welcome in, {name}")
speak(f"Welcome in, {name}")


# download index number


def Check_index():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('index').get()

def Check_bass():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('Bass').get()

def Check_mid():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('Mid').get()

def Check_treble():
    return root.child(f'{macAdress}').child('users').child(f'{current_user}').child('Treble').get()

# set index
chord_index = Check_index()

# set equalizer values
bass = Check_bass()
mid = Check_mid()
treble = Check_treble()

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
        if index <= 2:      # global instruments
            storage_path = rf"sounds{index}/{note['note']}.wav"
        else:               # user specific instruments
            storage_path = rf"users/{current_user}/sounds{index}/{note['note']}.wav"

        # download the sound file to a temporary file
        temp_file = rf"/home/pi/Desktop/cloudwave/sound/{note['note']}.wav"
        blob = bucket.blob(storage_path)
        blob.download_to_filename(temp_file)

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        print(f"finished downloading {note['note']}.wav")
    return FXBoard


# uploading song to firebase
def Upload_file(name):
    path = rf"/home/pi/Desktop/cloudwave/sound"
    upload_path = rf"users/{current_user}/Saved_music/{name}.wav"
    blob = bucket.blob(upload_path)
    blob.upload_from_filename(fr'{path}\{name}.wav')
    print("Upload successful")
    speak("Upload successful")

# update without overwriting from firebase

def Update_Chords(index):
    FXBoard = []
    for note in Chords:
        temp_file = rf"/home/pi/Desktop/cloudwave/sound/{note['note']}.wav"

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        # print(f"finished downloading {note['note']}.wav")
    return FXBoard


recording = []


def record(sound, state):
    path = rf"/home/pi/Desktop/cloudwave/sound"
    if state:
        recording.append(sound)
    else:
        # Open the WAV file for writing
        with wave.open(fr"{path}\new_song.wav", "wb") as wav_file:
            # Set the number of channels and sample width
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)        # 2 or 4
            wav_file.setframerate(44100)    # 44100 or 48000

            # Write each sound to the WAV file
            for sound in recording:
                sound_data = sound.get_raw()
                wav_file.writeframes(sound_data)
        recording.clear()
        Upload_file("new_song")         # upload to firebase
        speak("Song uploaded")


def change_pitch(Sounds, semitones):
    pitched = []
    i = 0
    if semitones == 0:      # 0 pitch
        pitched = Update_Chords(chord_index)
    else:
        for note in Chords:
            # path = rf"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp"
            path = rf"/home/pi/Desktop/cloudwave/sound"
            with wave.open(fr"{path}/{note['note']}pitched.wav", "wb") as wav_file:
                # Set the number of channels and sample width
                if semitones == -1:      #pitch down
                    wav_file.setnchannels(1)        # 1 or 2
                    wav_file.setsampwidth(2)        # 2 or 4
                elif semitones == 1:    # pitch up
                    wav_file.setnchannels(2)  # 1 or 2
                    wav_file.setsampwidth(4)  # 2 or 4

                wav_file.setframerate(44100)  # 44100 or 48000
                sound_data = Sounds[i].get_raw()
                wav_file.writeframes(sound_data)
            pitched.append(pygame.mixer.Sound(fr"{path}/{note['note']}pitched.wav"))
            i += 1
    return pitched

# download chords
SoundBoard = Download_Chords(chord_index)

# set original pitch
SoundBoard = change_pitch(SoundBoard, 0)

# check and update equalizer
# SoundBoard = equalizerSet(bass, treble, mid)
# SoundBoard = equalizerSet(0, 0, 0)


is_recording = False    # recording state
volume_octave = False   # False = volume    True = octave
octave = 0
song = None            # appending sounds for recording
try:
    while True:
        # change volume or change octave
        if GPIO.input(15) == 0 and volume_octave is False:
            time.sleep(0.25)                      # minska volym
            change_volume(15)
        elif GPIO.input(14) == 0 and volume_octave is False:
            time.sleep(0.25)                    # öka volym
            change_volume(14)
        if GPIO.input(16) == 0 and octave >= 0:
            time.sleep(0.25)    # minska octav
            octave -= 1
            SoundBoard = change_pitch(SoundBoard, octave)
        elif GPIO.input(20) == 0 and octave <= 0:
            time.sleep(0.25)     # öka octav
            octave += 1
            SoundBoard = change_pitch(SoundBoard, octave)

        # recording music and uploading
        if GPIO.input(17) == 0 and is_recording is False:
            speak("Recording in progress")
            is_recording = True
        elif GPIO.input(17) == 0 and is_recording is True:
            record(None, False)     # stop recording, save, and upload
            speak("Recording stopped")
            is_recording = False
        if is_recording is True and Song is not None:
            record(Song, True)
            Song = None

        # change soundboard if index differ
        if chord_index != Check_index():
            chord_index = Check_index()
            SoundBoard = Download_Chords(chord_index)

        # update equalizer values
        if bass != Check_bass() or treble != Check_treble() or mid != Check_mid():
            bass = Check_bass()
            treble = Check_treble()
            mid = Check_mid()
            SoundBoard = equalizerSet(bass, mid, treble, octave)


        # if button pressed, play sound
        if GPIO.input(4) == 0:
            print("Sound C")      # play sound
            SoundBoard[0].play()                # plays sound at index
            Song = SoundBoard[0]
            time.sleep(0.25)
        if GPIO.input(27) == 0:
            print("Sound D")      # play sound
            SoundBoard[1].play()   # plays sound at index
            Song = SoundBoard[1]
            time.sleep(0.25)
        if GPIO.input(22) == 0:
            print("Sound E")      # play sound
            SoundBoard[2].play()   # plays sound at index
            Song = SoundBoard[2]
            time.sleep(0.25)
        if GPIO.input(5) == 0:
            print("Sound F")  # play sound
            SoundBoard[3].play()  # plays sound at index
            Song = SoundBoard[3]
            time.sleep(0.25)
        if GPIO.input(6) == 0:
            print("Sound G")      # play sound
            SoundBoard[4].play()  # plays sound at index
            Song = SoundBoard[4]
            time.sleep(0.25)
        if GPIO.input(26) == 0:
            print("Sound A")      # play sound
            SoundBoard[5].play()  # plays sound at index
            Song = SoundBoard[5]
            time.sleep(0.25)
        if GPIO.input(23) == 0:
            print("Sound B")      # play sound
            SoundBoard[6].play()  # plays sound at index
            Song = SoundBoard[6]
            time.sleep(0.25)
        if GPIO.input(25) == 0:
            print("Sound C# ")      # play sound
            SoundBoard[7].play()  # plays sound at index
            Song = SoundBoard[7]
            time.sleep(0.25)
        if GPIO.input(2) == 0:
            print("Sound D#")      # play sound
            SoundBoard[8].play()  # plays sound at index
            Song = SoundBoard[8]
            time.sleep(0.25)
        if GPIO.input(3) == 0:
            print("Sound F#")      # play sound
            SoundBoard[9].play()  # plays sound at index
            Song = SoundBoard[9]
            time.sleep(0.25)
        if GPIO.input(24) == 0:
            print("Sound G#")      # play sound
            SoundBoard[10].play()  # plays sound at index
            Song = SoundBoard[10]
            time.sleep(0.25)
        if GPIO.input(8) == 0:
            print("Sound A#")      # play sound
            SoundBoard[11].play()  # plays sound at index
            Song = SoundBoard[11]
            time.sleep(0.25)
except KeyboardInterrupt:
    pygame.mixer.stop()
    GPIO.cleanup()
