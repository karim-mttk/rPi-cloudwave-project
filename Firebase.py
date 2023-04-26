import firebase_admin
from firebase_admin import credentials, storage, db

import pygame
from pygame import time

# initialize Pygame mixer for playing sound files
pygame.mixer.init()

# cred = credentials.Certificate(r"firebasekey.json")
cred = credentials.Certificate(r"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\firebase key\cloudwave-test-firebase-adminsdk-ejn2w-6a4e295421.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'cloudwave-test.appspot.com', 'databaseURL': 'https://cloudwave-test-default-rtdb.europe-west1.firebasedatabase.app'})

# create a Firebase Storage client
bucket = storage.bucket()
root = db.reference("/")

# download index number
# index_path = 'index.txt'
# change to RPi storage path later
# index_temp_file = r'index.txt'
# index_temp_file = r"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\index.txt"

# blob = bucket.blob(index_path)
# blob.download_to_filename(index_temp_file)
# with open(index_temp_file) as file:
#     index = file.read()

def Check_index():
    return int(root.child('index').get())


index = Check_index()


# alternative method for selecting chords
Chords = [{"note": "C"}, {"note": "D"}, {"note": "E"}, {"note": "F"},
          {"note": "G"}, {"note": "A"}, {"note": "B"}, {"note": "C#"},
          {"note": "D#"}, {"note": "F#"}, {"note": "G#"}, {"note": "A#"}]

# download all chords and put in local storage
# all_chords = []
# IndexPath = 0
# for note in Chords:
    # specify the path to the audio file in Firebase Storage
#     storage_path = rf"sounds{index}/folder/{note['note']}.wav"

    # download the sound file to a temporary file
    # change to RPi storage path later
    # temp_file = rf"/home/pi/Desktop/programming/cloudwave/sound/{note['note']}.wav"
#     temp_file = rf"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp\{note['note']}.wav"
#     blob = bucket.blob(storage_path)
#     blob.download_to_filename(temp_file)

    # load the sound file into Pygame mixer and save it
#     all_chords.append(pygame.mixer.Sound(temp_file))
#     IndexPath += 1




def Download_Chords(index):
    FXBoard = []
    for note in Chords:
        # specify the path to the audio file in Firebase Storage

        storage_path = rf"sounds{index}/folder/{note['note']}.wav"
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

# upload the audio file to Firebase Storage
# blob = bucket.blob(storage_path)
# blob.upload_from_filename(file_path)

# play all sounds, wait for each sound to finish playing
while True:
    i = 0
    for note in Chords:
        if index != Check_index():
            index = Check_index()
            SoundBoard = Download_Chords(index)
        else:
            SoundBoard[i].play()
            i += 1
            print(Check_index())
            while pygame.mixer.get_busy():
                pass

