import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

#This works better than pyttsx3 on the pi 4 with 2 gb
def tts(message):
    model = "en_US-lessac-medium.onnx"
    voice = PiperVoice.load(model)
    stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
    stream.start()

    for audio_bytes in voice.synthesize_stream_raw(message):
        int_data = np.frombuffer(audio_bytes, dtype=np.int16)
        stream.write(int_data)
    stream.stop()
    stream.close()