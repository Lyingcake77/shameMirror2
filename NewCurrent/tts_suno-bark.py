from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, BarkModel
import numpy as np
import sounddevice as sd

def tts(message):
    processor = AutoProcessor.from_pretrained("suno/bark")
    model = BarkModel.from_pretrained("suno/bark")
    inputs = processor(message + "[laughs]", voice_preset="v2/en_speaker_5")

    audio_array = model.generate(**inputs)
    audio_array = audio_array.cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    #scipy.io.wavfile.write("bark_out.wav",rate=sample_rate, data=audio_array)

    stream = sd.OutputStream(samplerate=sample_rate, channels=1, dtype='int16')
    stream.start()

    for audio_bytes in audio_array:
        int_data = np.frombuffer(audio_bytes, dtype=np.int16)
        stream.write(int_data)
    stream.stop()
    stream.close()