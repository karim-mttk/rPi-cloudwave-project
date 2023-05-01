
import RPi.GPIO as GPIO
import time
import pygame
import numpy as np
import wave

import firebase_admin
from firebase_admin import credentials, storage, db

# pygame setup
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

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


# function to redefine index from firebase in main loop later
macAdress = "dc:a6:32:b4:da:a5"


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
            CurrentUser = Device.child('Current User').get()
            User = Device.child(f'{CurrentUser}')
            User_password = User.child('synthPassword').get()

            Input_password = type_synth_password()
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

# function for saving and uploading recorded music. may have problems with interpreting "empty space"
# and multiple button presses at the same time

def record_music(song):
    # Combine the recorded audio into a single Pygame Sound object
    recording_array = np.concatenate([pygame.sndarray.array(s) for s in song])
    recording_sound = pygame.sndarray.make_sound(recording_array)

    # convert to wav file
    save = wave.open(
        fr'/home/pi/Desktop/programming/cloudwave/sound/new_song.wav', 'w')

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
    blob.upload_from_filename(
        fr'/home/pi/Desktop/programming/cloudwave/sound/new_song.wav')

    print(f"finished uploading new_song.wav")



try:
    while True:
        #sudo
        #if recording == 1:
        #

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


