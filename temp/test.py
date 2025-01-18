#from ollama import chat
#from ollama import ChatResponse
import pyttsx3
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice
import wave
'''
response: ChatResponse = chat(model='llama2-uncensored', messages=[
  {
    'role': 'user',
   #'content': 'Generate an insult based on the following features about their face: "large nose, crooked teeth, and an asymmetrical face"',
    'content': 'Generate an insult based on the following criteria: there is a man with a beard and a mustache in a room',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)
'''
model = "en_US-lessac-medium.onnx"
voice = PiperVoice.load(model)
text = "This is an example of text to speech"
#wav_file = wave.open("output.wav", "w")

#audio = voice.synthesize(text, wav_file)

stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
stream.start()

for audio_bytes in voice.synthesize_stream_raw(text):
    int_data = np.frombuffer(audio_bytes, dtype=np.int16)
    stream.write(int_data)
stream.stop()
stream.close()
'''
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
print(voices[0])
#engine.setProperty('voice', voices[].id)
engine.say("Generate an insult based on the following criteria: there is a man with a beard and a mustache in a room")
engine.runAndWait()
engine.stop()
'''