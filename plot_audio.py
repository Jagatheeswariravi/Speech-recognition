import wave
import matplotlib.pyplot as plt
import numpy as np

obj = wave.open("Wav_868kb.wav","rb")

sample_rate = obj.getframerate()
n_frames = obj.getnframes()
n_channels = obj.getnchannels()
signal_wave =obj.readframes(-1)

obj.close()

t_audio = n_frames/sample_rate

print(t_audio)

signal_array = np.frombuffer(signal_wave,dtype=np.int16)


times = np.linspace(0,t_audio,num=n_frames*2)

plt.figure(figsize=(10,10))
plt.plot(times,signal_array)
plt.xlabel("time in second")
plt.ylabel("signal_wave")
plt.xlim(0,t_audio)
plt.show()