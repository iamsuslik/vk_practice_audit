import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

fs = 44100
duration = 3
print("Говорите...")
recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
sd.wait()
wav.write("modules/test_audio.wav", fs, recording)
print("Файл test_audio.wav создан.")