import wave

obj = wave.open("Wav_868kb.wav","rb")

print("the number of channels",obj.getnchannels())

print("The sampling rate",obj.getframerate())
print("The number of frame",obj.getnframes())

frames = obj.readframes(-1)

print(type(frames))

print(type(frames[0]))

obj.close()

obj_new = wave.open("new.wav","wb")

obj_new.setnchannels(2)
obj_new.setsampwidth(2)
obj_new.setframerate(44100)
obj_new.writeframes(frames)
obj_new.close()
