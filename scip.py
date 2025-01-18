from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
'''
processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")
inputs = processor("""[laughs] You human paraquat! """, voice_preset="v2/en_speaker_5")

audio_array = model.generate(**inputs)
audio_array = audio_array.cpu().numpy().squeeze()
sample_rate = model.generation_config.sample_rate
scipy.io.wavfile.write("bark_out.wav",rate=sample_rate, data=audio_array)
'''
# download and load all models
preload_models()

# generate audio from text
text_prompt = """
     Hello, my name is Suno. And, uh... and I like pizza. [laughs] But I also have other interests such as playing tic tac toe.
"""
speech_array = generate_audio(text_prompt)


write_wav("NewCurrent/audio/00000000-0000-0000-0000-000000000000.wav", SAMPLE_RATE, speech_array)