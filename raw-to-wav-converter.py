import wave

path = fr'/home/pi/Desktop/programming/cloudwave'


def converter():
    # Open the raw audio file
    with open(fr'{path}\input.raw', 'rb') as raw_file:
        raw_data = raw_file.read()

    # Create a new WAV file
    with wave.open(fr'{path}\output.wav', 'wb') as wav_file:
        # Set the parameters for the WAV file
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)

        # Write the raw data to the WAV file
        wav_file.writeframesraw(raw_data)
