import firebase_admin
from firebase_admin import credentials, storage, db, auth

import pygame
import pyttsx3
from eq_test import equalizerSet
from python_Scr_C_record import record
from raw-to-wav-converter import converter

import pyaudio
import wave

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
            User_password = User.child('synthPassword').get()


            print("Type password:")
            # speak("Type password")
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
print("User Authenticated")
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


def change_pitch(sound, pitch):
    # do for all 12 notes
    # pitch up or down, 2 is up, 0,5 is down
    sound.set_speed(pitch)


speak("Recording in progress")
i = 0
record()
while True:
    if index != Check_index():
        index = Check_index()
        SoundBoard = Download_Chords(index)

    for j in Song2:
        SoundBoard[Song2[i]].play()
        print(Check_index())
        i += 1

    break
# speak("Recording stopped")

# Save the recorded audio in a WAV file
# path = fr"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp"
path = fr'/home/pi/Desktop/programming/cloudwave'

converter()

# upload to firebase
# upload_path = rf"{current_user}/Saved_Music/new_song.wav"
# blob = bucket.blob(upload_path)
# blob.upload_from_filename(fr'{path}\output.wav')

print(f"finished uploading new_song.wav")

