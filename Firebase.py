import firebase_admin
from firebase_admin import credentials, storage, db

import pygame
import numpy as np
import soundcard as sc
import pyttsx3
from scipy.io.wavfile import write
# from eq_test import equalizerSet

import sounddevice as sd
#check audio devices
# print(sd.query_devices())



# initialize Pygame mixer for playing sound files
# pygame.mixer.init()
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)


# cred = credentials.Certificate(r"firebasekey.json")
cred = credentials.Certificate(r"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\firebase key\cloudwave-test-firebase-adminsdk-ejn2w-6a4e295421.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'cloudwave-test.appspot.com', 'databaseURL': 'https://cloudwave-test-default-rtdb.europe-west1.firebasedatabase.app'})

# create a Firebase Storage client
bucket = storage.bucket()
root = db.reference("/")
macAdress = "dc:a6:32:b4:da:a5"

# validate user id

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
            CurrentUser = Device.child('Current User').get()
            User = Device.child(f'{CurrentUser}')
            User_password = User.child('synthPassword').get()

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
print("User Authenticated")
# download index number


def Check_index():
    return root.child(f'{macAdress}').child(f'{current_user}').child('index').get()


index = Check_index()


# alternative method for selecting chords
Chords = [{"note": "C"}, {"note": "D"}, {"note": "E"}, {"note": "F"},
          {"note": "G"}, {"note": "A"}, {"note": "B"}, {"note": "C#"},
          {"note": "D#"}, {"note": "F#"}, {"note": "G#"}, {"note": "A#"}]

# download all chords and put in local storage

Song = [{"note": "D"}, {"note": "D"}, {"note": "D"}, {"note": "A"}, {"note": "G#"}, {"note": "G"}, {"note": "F"},
        {"note": "D"}, {"note": "F"}, {"note": "G"}, {"note": "C"}, {"note": "C"}]

Song2 = [1, 1, 1, 5, 10, 4, 3, 1, 3, 4, 0, 0]

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
        blob = bucket.blob(storage_path)
        blob.download_to_filename(temp_file)

        # load the sound file into Pygame mixer and save it
        FXBoard.append(pygame.mixer.Sound(temp_file))
        print(f"finished downloading {note['note']}.wav")
    return FXBoard


SoundBoard = Download_Chords(index)

recording = []

# get a list of all speakers:
speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()

# get a list of all microphones:v
mics = sc.all_microphones(include_loopback=True)
# get the current default microphone on your system:
default_mic = mics[1]

# play all sounds, wait for each sound to finish playing
start_time = pygame.time.get_ticks()

with default_mic.recorder(samplerate=44100) as mic, \
            default_speaker.player(samplerate=44100) as sp:
    frames = []
    num_frames = 44100 * 0.5 # record for 5 seconds
    data = 0
while True:
    i = 0
    print("next")
    for note in Song:
        if index != Check_index():
            index = Check_index()
            SoundBoard = Download_Chords(index)
        SoundBoard[Song2[i]].play()

        # for j in range(0, int(44100 / num_frames * num_frames)):
        data = default_mic.record(numframes=num_frames, samplerate=44100)
        frames.append(data)

        i += 1
        print(Check_index())
        # while pygame.mixer.get_busy():
        #     pass
    # Stop recording after 30 seconds
    print(pygame.time.get_ticks() - start_time)
    if pygame.time.get_ticks() - start_time >= 5000:
        break


path = fr"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\new_song.wav"
frames = np.concatenate(frames)
frames /= 1.414
frames *= 32767
int16_data = frames.astype(np.int16)
write(path, 44100, int16_data)


# upload to firebase
upload_path = rf"{current_user}/Saved_Music/new_song.wav.wav"
blob = bucket.blob(upload_path)
blob.upload_from_filename(fr'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\new_song.wav')

print(f"finished uploading new_song.wav")

