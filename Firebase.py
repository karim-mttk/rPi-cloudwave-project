import firebase_admin
from firebase_admin import credentials, storage, db

import pygame
import numpy as np
import wave

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


def validate_synth_password():
    while True:
        try:
            # find device, find current user, and find current user password
            Device = root.child(f'{macAdress}')
            CurrentUser = Device.child('Current User').get()
            User = Device.child(f'{CurrentUser}')
            User_password = User.child('synthPassword').get()

            print("Type password:")
            Input_password = input()
            if Input_password == User_password:
                break
            else:
                print("Wrong password")
        except:
            print("Exception, user not found")
    return CurrentUser


current_user = validate_synth_password()

# download index number


def Check_index():
    return root.child(f'{macAdress}').child(f'{current_user}').child('index').get()


index = Check_index()


# alternative method for selecting chords
Chords = [{"note": "C"}, {"note": "D"}, {"note": "E"}, {"note": "F"},
          {"note": "G"}, {"note": "A"}, {"note": "B"}, {"note": "C#"},
          {"note": "D#"}, {"note": "F#"}, {"note": "G#"}, {"note": "A#"}]

# download all chords and put in local storage


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

channel = pygame.mixer.Channel(0)

# upload the audio file to Firebase Storage
# blob = bucket.blob(storage_path)
# blob.upload_from_filename(file_path)

# play all sounds, wait for each sound to finish playing
start_time = pygame.time.get_ticks()
while True:
    i = 0
    print("next")
    for note in Chords:
        if index != Check_index():
            index = Check_index()
            SoundBoard = Download_Chords(index)
        SoundBoard[i].play()
        recording.append(SoundBoard[i])
        i += 1
        print(Check_index())
        while pygame.mixer.get_busy():
            pass
    # Stop recording after 30 seconds
    print(pygame.time.get_ticks() - start_time)
    if pygame.time.get_ticks() - start_time >= 30000:
        break

pygame.mixer.stop()

# Combine the recorded audio into a single Pygame Sound object
recording_array = np.concatenate([pygame.sndarray.array(s) for s in recording])
recording_sound = pygame.sndarray.make_sound(recording_array)

# convert to wav file
save = wave.open(fr'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\new_song.wav', 'w')

# set the parameters
save.setframerate(44100)
save.setnchannels(2)
save.setsampwidth(2)

# write raw PyGame sound buffer to wave file
save.writeframesraw(recording_sound.get_raw())

# close file
save.close()

# upload to firebase
upload_path = rf"{current_user}/Saved_Music/new_song.wav.wav"
blob = bucket.blob(upload_path)
blob.upload_from_filename(fr'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\new_song.wav')

print(f"finished uploading new_song.wav")

