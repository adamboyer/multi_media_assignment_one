import numpy as np
import os
import librosa
from playsound import playsound
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
def remove_high_freq(filename):
    signal, sr = librosa.load(os.path.join(".", filename))
    duration = librosa.get_duration(y=signal, sr=sr)
    # normalize the tone 
    normalize_tone = np.float32(signal/ np.max(np.abs(signal)) * 1)
    N = int(sr * duration)
    # Find fft
    yf = rfft(normalize_tone)
    xf = rfftfreq(N, 1 / sr)

    # filter out frequencies above 8000
    points_per_freq = len(xf) / (sr / 2)
    target_idx = int(points_per_freq * 3000)
    yf[target_idx - 1:] = 0;

    # perform invers fft
    new_sig = irfft(yf)

    # normalize new signal
    norm_new_sig = np.float32(new_sig * (1 / new_sig.max()))
    write("new_"+filename,sr, norm_new_sig) 

    #fourier_transform = np.fft.fft(signal)
    #print(fourier_transform)
    
    # find the magnitudes
    #magnitude_spectrum = np.abs(fourier_transform)

    # find the frequencies
    #freq = np.linspace(0, sr, len(magnitude_spectrum))

    # filter out the high frequencies
    #freq = list(filter(filter_high_freq, freq))

    # inverse fourier_transform
    #new_signal = np.fft.ifft(freq)
    #print("here is the new signal")
    #print(new_signal)

    # create a new wav file 
    #scaled_data = np.float32(freq / np.max(np.abs(new_signal)) * 1)
    #write('new_'+filename, sr, scaled_data)

    return 'new_' + filename

# function to play wave file
def play_wav(filename):
    audio = AudioSegment.from_wav(filename)
    play(audio)
# Names of the audio files
talking_file = "me_talking.wav"
piano_file = "piano.wav"
violin_file = "violin.wav"
loud_file = "loud_pitch.wav"
talking_high_pitch = "high_pitch.wav"

#play audio files
print("Welcome!")
print("First I will play an audio file of a piano playing...")
#play_wav(piano_file)
#new_piano_file = remove_high_freq(piano_file)
#new_talking_file = remove_high_freq(talking_file)
remove_high_freq(talking_high_pitch)
#print("Now here is the same file with frequencies 8Hz and above removed")
#play_wav(new_piano_file)
# Load the audio files into np arrays
talking, sr = librosa.load(os.path.join(".", talking_file))
piano, sr = librosa.load(os.path.join(".", piano_file))
violin, sr = librosa.load(os.path.join(".", talking_file))



# pip install ffmpeg
# pip install numpy
# pip install pydub
# pip install scipy
# python -W ignore fourier_transform.py

