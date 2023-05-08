import firebase_admin
from firebase_admin import credentials, storage, db

import pygame
import pyttsx3
import wave
from eq_test import equalizerSet
from python_Scr_C_record import record
# from raw_to_wav_converter import converter

import pyaudio
from pydub import AudioSegment
import librosa
import numpy as np

# Define audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024

# initialize Pygame mixer for playing sound files
pygame.init()
pygame.mixer.init(frequency=44100, size=16, channels=2, buffer=4096)


#cred = credentials.Certificate(r"firebasekey.json")
cred = credentials.Certificate(r"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\firebase key\cloudwave-test-firebase-adminsdk-ejn2w-6a4e295421.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'cloudwave-test.appspot.com', 'databaseURL': 'https://cloudwave-test-default-rtdb.europe-west1.firebasedatabase.app'})

# create a Firebase Storage client
bucket = storage.bucket()
root = db.reference("/")
# root = root.child('CloudWave')
macAdress = "dc:a6:32:b4:da:a5"

# parent_node_ref = db.reference(f'/{macAdress}')

# Add a child node to a child node
# child_node_ref = parent_node_ref.child('user1').push()

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def validate_synth_password():
    while True:
        try:
            # find device, find current user, and find current user password
            Device = root.child(f'{macAdress}')
            CurrentUser = Device.child('CurrentUser').child('User').get()
            User = Device.child('users').child(f'{CurrentUser}')
            print(CurrentUser)
            User_password = User.child('SynthPassword').get()
            print(User_password)

            print("Type password:")
            speak("Type password")
            Input_password = input()
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


index = Check_index()


# alternative method for selecting chords
Chords = [{"note": "C"}, {"note": "D"}, {"note": "E"}, {"note": "F"},
          {"note": "G"}, {"note": "A"}, {"note": "B"}, {"note": "C#"},
          {"note": "D#"}, {"note": "F#"}, {"note": "G#"}, {"note": "A#"}]

# Song2 = [1, 1, 1, 5, 10, 4, 3, 1, 3, 4, 0, 0]
Song2 = [3, 3, 10, 11, 11, 10, 3, 3, 10, 11, 11, 10, 3, 8, 3, 11, 10, 3, 8, 3]

# equalizerSet()

def Download_Chords(index):
    FXBoard = []
    for note in Chords:
        # specify the path to the audio file in Firebase Storage

        # storage_path = rf"sounds{index}/folder/{note['note']}.wav"
        storage_path = rf"{current_user}/sounds{index}/{note['note']}.wav"

        # download the sound file to a temporary file
        # change to RPi storage path later
        temp_file = rf"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\{note['note']}.wav"
        # temp_file = rf"/home/pi/Desktop/programming/cloudwave/sound/{note['note']}.wav"
        blob = bucket.blob(storage_path)
        blob.download_to_filename(temp_file)

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        print(f"finished downloading {note['note']}.wav")
    return FXBoard


SoundBoard = Download_Chords(index)

# Initialize PyAudio
# p = pyaudio.PyAudio()

# Get the index of the Stereo Mix input device (assuming it's available on your computer)
# input_device_index = None
# info = p.get_host_api_info_by_index(0)
# num_devices = info.get('deviceCount')
# for i in range(num_devices):
#     if "stereo mix" in p.get_device_info_by_host_api_device_index(0, i).get('name').lower():
#         input_device_index = i

# If the Stereo Mix input device is not available, print an error message and exit
# if input_device_index is None:
#     print("Stereo Mix input device not found")
#     exit()
# Get the index of the onboard audio input device





def change_pitch(Sounds, semitones):
    pitched = []
    i = 0
    if semitones == 0:
        pitched = Update_Chords(index)
    else:
        for note in Chords:
            path = rf"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp"
            with wave.open(fr"{path}\{note['note']}pitched.wav", "wb") as wav_file:
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
            pitched.append(pygame.mixer.Sound(fr"{path}\{note['note']}pitched.wav"))
            i += 1
    return pitched

def Update_Chords(index):
    FXBoard = []
    for note in Chords:
        temp_file = rf"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\{note['note']}.wav"

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        print(f"finished downloading {note['note']}.wav")
    return FXBoard

# record music, rudimentary
recording = []

def record(sound, state):
    path = fr"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp"
    if state:
        recording.append(sound)
    else:
        # Open the WAV file for writing
        with wave.open(fr"{path}\output2.wav", "wb") as wav_file:
            # Set the number of channels and sample width
            wav_file.setnchannels(2)
            wav_file.setsampwidth(2)    # 2 or 4
            wav_file.setframerate(44100)    # 44100 or 48000

            # Write each sound to the WAV file
            for sound in recording:
                sound_data = sound.get_raw()
                wav_file.writeframes(sound_data)



def Upload_file(name):
    upload_path = rf"{current_user}/Saved_Music/{name}.wav"
    blob = bucket.blob(upload_path)
    blob.upload_from_filename(fr'{path}\output.wav')
    print("Upload successful")
    speak("Upload successful")


SoundBoard = change_pitch(SoundBoard, 1)
# SoundBoard = Update_Chords(index)

speak("Recording in progress")
i = 0

start_time = pygame.time.get_ticks()
while True:
    if index != Check_index():
        index = Check_index()
        SoundBoard = Download_Chords(index)

    for j in Song2:
        SoundBoard[Song2[i]].play()
        record(SoundBoard[Song2[i]], True)
        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 500:
            pass

        print(Check_index())
        i += 1

    break
record(None, False)
speak("Recording stopped")

# Save the recorded audio in a WAV file
path = fr"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp"
# path = fr'/home/pi/Desktop/programming/cloudwave'

# converter()

# upload to firebase
# upload_path = rf"{current_user}/Saved_Music/new_song.wav"
# blob = bucket.blob(upload_path)
# blob.upload_from_filename(fr'{path}\output.wav')

print(f"finished uploading new_song.wav")

