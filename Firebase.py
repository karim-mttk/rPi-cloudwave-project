import firebase_admin
from firebase_admin import credentials, storage, db

import pygame

# initialize Pygame mixer for playing sound files
pygame.mixer.init()

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
        SoundBoard[i].play()
        i += 1
        print(Check_index())
        while pygame.mixer.get_busy():
            pass

