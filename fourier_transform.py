import numpy as np
import os
import librosa
import time
from scipy.io.wavfile import write
from scipy.fft import rfft, rfftfreq, irfft
from pydub import AudioSegment
from pydub.playback import play

# Simple filter function
def filter_high_freq(freq):
    if freq < 8:
        return True
    else:
        return False

# Perform Fourier transform, remove high frequencies, and create new audio file
def remove_high_freq(filename, hz):
    signal, sr = librosa.load(os.path.join(".", filename))
    duration = librosa.get_duration(y=signal, sr=sr)

    # normalize the tone 
    norm_signal = np.int16((signal/ signal.max()) * 32767)
    N = int(sr * duration)
    # Find fft
    yf = rfft(norm_signal)
    xf = rfftfreq(N, 1 / sr)

    # filter out frequencies above 8000
    points_per_freq = len(xf) / (sr / 2)
    target_idx = int(points_per_freq * hz)
    yf[target_idx - 1:] = 0;

    # perform inverse fft
    new_signal = irfft(yf)

    # normalize new signal
    norm_new_signal = np.int16(new_signal * (32767 / new_signal.max()))
    write("new_"+filename,sr, norm_new_signal) 

    return "new_" + filename

# function to play wave file
def play_wav(filename):
    audio = AudioSegment.from_wav(filename)
    play(audio)
# Names of the audio files
piano_file = "piano_c_3_major.wav"
talking_high_pitch = "high_pitch.wav"

#play audio files
print("Welcome!")
print("First I will play an audio file of me talking with a loud pitch...")
time.sleep(1)
play_wav(talking_high_pitch)
new_talking = remove_high_freq(talking_high_pitch, 3000)
print("Now I will play the same file with frequencies 3000Hz and above removed")
time.sleep(1)
play_wav(new_talking)
print("Wow! No high pitch noise!")
print("Here is the C3 major scale for the piano")
time.sleep(1)
play_wav(piano_file)
new_piano = remove_high_freq(piano_file, 500)
print("Now here is the same scale but with only frequencies 500Hz and below")
time.sleep(1)
play_wav(new_piano)
print("You will notice that the higher harmonics are now gone")
