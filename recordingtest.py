import RPi.GPIO as GPIO
import alsaaudio
import wave

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)

# Set up ALSA mixer
mixer = alsaaudio.Mixer(control='Headphone', cardindex=2)

# Define callback function to adjust volume
def change_volume(channel):
    volume = alsaaudio.Mixer(control='Headphone', cardindex=2).getvolume()[0]
    if channel == 27 and volume < 100:
        mixer.setvolume(volume+1)

# Add event detection to GPIO
GPIO.add_event_detect(27, GPIO.RISING, callback=change_volume)

# Set up audio recording
card = 'bcm2835 Headphones'
device = 'default'
wav_output = wave.open('recording.wav', 'wb')
wav_output.setnchannels(2)
wav_output.setsampwidth(2)
wav_output.setframerate(44100)

# Record audio when GPIO17 is high
while True:
    if GPIO.input(17) == GPIO.HIGH:
        # Start recording
        print("Recording started")
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK, card=card, device=device)
        inp.setchannels(2)
        inp.setrate(44100)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(1024)
        frames = []
        while GPIO.input(17) == GPIO.HIGH:
            l, data = inp.read()
            if l:
                frames.append(data)
                wav_output.writeframes(data)
        # Stop recording
        print("Recording stopped")
        inp.close()
        wav_output.close()
