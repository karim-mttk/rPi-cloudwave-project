#include <stdio.h>
#include <stdlib.h>
#include <alsa/asoundlib.h>

#define PCM_DEVICE "default"
#define SAMPLE_RATE 44100
#define CHANNELS 2
#define BUFFER_SIZE 4096

int main(int argc, char **argv)
{
    int err;
    snd_pcm_t *handle;
    snd_pcm_hw_params_t *hw_params;
    snd_pcm_uframes_t frames;
    char *buffer;
    int size;

    // Open PCM device
    err = snd_pcm_open(&handle, PCM_DEVICE, SND_PCM_STREAM_CAPTURE, 0);
    if (err < 0) {
        printf("Error opening PCM device: %s\n", snd_strerror(err));
        exit(1);
    }

    // Allocate hardware parameters object
    snd_pcm_hw_params_alloca(&hw_params);

    // Set hardware parameters
    err = snd_pcm_hw_params_any(handle, hw_params);
    if (err < 0) {
        printf("Error setting hardware parameters: %s\n", snd_strerror(err));
        exit(1);
    }
    err = snd_pcm_hw_params_set_access(handle, hw_params, SND_PCM_ACCESS_RW_INTERLEAVED);
    if (err < 0) {
        printf("Error setting access type: %s\n", snd_strerror(err));
        exit(1);
    }
    err = snd_pcm_hw_params_set_format(handle, hw_params, SND_PCM_FORMAT_S16_LE);
    if (err < 0) {
        printf("Error setting format: %s\n", snd_strerror(err));
        exit(1);
    }
    err = snd_pcm_hw_params_set_channels(handle, hw_params, CHANNELS);
    if (err < 0) {
        printf("Error setting channels: %s\n", snd_strerror(err));
        exit(1);
    }
    unsigned int sample_rate = SAMPLE_RATE;
    err = snd_pcm_hw_params_set_rate_near(handle, hw_params, &sample_rate, 0);
    if (err < 0) {
        printf("Error setting sample rate: %s\n", snd_strerror(err));
        exit(1);
    }

    // Apply hardware parameters
    err = snd_pcm_hw_params(handle, hw_params);
    if (err < 0) {
        printf("Error setting hardware parameters: %s\n", snd_strerror(err));
        exit(1);
    }

    // Calculate buffer size
    snd_pcm_hw_params_get_period_size(hw_params, &frames, 0);
    size = frames * CHANNELS * 2; // 2 bytes per sample

    // Allocate buffer
    buffer = (char *) malloc(size);

    // Start capturing audio
    while (1) {
        err = snd_pcm_readi(handle, buffer, frames);
        if (err < 0) {
            printf("Error reading from PCM device: %s\n", snd_strerror(err));
            break;
        }
        fwrite(buffer, 1, size, stdout);
    }

    // Cleanup
    free(buffer);
    snd_pcm_close(handle);
    return 0;
}
