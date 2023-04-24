import firebase_admin
from firebase_admin import credentials, storage

import pygame

cred = credentials.Certificate(r"C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\firebase key\cloudwave-test-firebase-adminsdk-ejn2w-6a4e295421.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'cloudwave-test.appspot.com'
})

# create a Firebase Storage client
bucket = storage.bucket()

# specify the path to the audio file on your local machine
file_path = r'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\Sound test/C_Major_Chord.wav'

# download index number
index_path = 'index.txt'
index_temp_file = r'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp/index.txt'
blob = bucket.blob(index_path)
blob.download_to_filename(index_temp_file)
with open(index_temp_file) as file:
    index = file.read()

# specify the path to the audio file in Firebase Storage
storage_path = rf'sounds{index}/folder/audio-file.mp3'

# upload the audio file to Firebase Storage
# blob = bucket.blob(storage_path)
# blob.upload_from_filename(file_path)

print('File {} uploaded to {}.'.format(file_path, storage_path))

# download the sound file to a temporary file
temp_file = r'C:\Users\anton\OneDrive\Dokument\1. Skolsaker\0. Projekt och Projektmetoder\Projekt\temp/sound-file.mp3'
blob = bucket.blob(storage_path)
blob.download_to_filename(temp_file)

# initialize Pygame mixer for playing sound files
pygame.mixer.init()

# load the sound file into Pygame mixer and play it
sound = pygame.mixer.Sound(temp_file)
sound.play()

# wait for the sound to finish playing
while pygame.mixer.get_busy():
    pass