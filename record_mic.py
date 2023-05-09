import pyaudio



import wave

frames_per_buffer = 3200

format = pyaudio.paInt16

channels = 1

frame_rate = 16000

p =pyaudio.PyAudio()

stream = p.open(
    format = format,
    channels = channels,
    rate = frame_rate,
    input = True,
    frames_per_buffer=frames_per_buffer

)


print("Start recording")

seconds = 5

frames = []

for i in range(0,int(frame_rate/frames_per_buffer*seconds)):
    data = stream.read(frames_per_buffer)
    frames.append(data)

stream.stop_stream()
stream.close()
p.terminate()


obj = wave.open("recording.wav","wb")

obj.setnchannels(channels)

obj.setframerate(frame_rate)

obj.setsampwidth(p.get_sample_size(format))

obj.writeframes(b"".join(frames))

obj.close()