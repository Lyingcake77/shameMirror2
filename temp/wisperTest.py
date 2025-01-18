from ollama import chat, Client
from ollama import ChatResponse
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

import random

client = Client(
  host='http://192.168.0.153:11434',
  #headers={'x-some-header': 'some-value'}
)
insults = ['large nose','has a cat', 'owns an iphone', 'crooked teeth', 'asymmetrical face', 'scar below the lip', 'mole under the right eye']
randomCharacteristics = random.sample(insults, 1)
print(randomCharacteristics)
response = client.chat(model='llama2-uncensored', messages=[
  {
    'role': 'user',
    'content': 'Generate an insult based on the following criteria:'+', '.join(randomCharacteristics),
  },
])
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

'''

model = "en_US-lessac-medium.onnx"
voice = PiperVoice.load(model)
text = response['message']['content']
print(text)
stream = sd.OutputStream(samplerate=voice.config.sample_rate, channels=1, dtype='int16')
stream.start()

for audio_bytes in voice.synthesize_stream_raw(text):
    int_data = np.frombuffer(audio_bytes, dtype=np.int16)
    stream.write(int_data)
stream.stop()
stream.close()