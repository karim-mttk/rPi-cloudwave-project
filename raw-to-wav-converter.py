import wave

def converter():
  # Open the raw audio file
  with open('input.raw', 'rb') as raw_file:
      raw_data = raw_file.read()

  # Create a new WAV file
  with wave.open('output.wav', 'wb') as wav_file:
      # Set the parameters for the WAV file
      wav_file.setnchannels(2)
      wav_file.setsampwidth(2)
      wav_file.setframerate(44100)

      # Write the raw data to the WAV file
      wav_file.writeframesraw(raw_data)
