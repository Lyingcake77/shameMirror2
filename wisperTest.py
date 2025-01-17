from ollama import chat
from ollama import ChatResponse
import pyttsx3

response: ChatResponse = chat(model='llama2-uncensored', messages=[
  {
    'role': 'user',
   #'content': 'Generate an insult based on the following features about their face: "large nose, crooked teeth, and an asymmetrical face"',
    'content': 'Generate an insult based on the following criteria: arafed man wearing a blue hat and sunglasses with a gold chain around his neck',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content)

engine = pyttsx3.init()
engine.say(response.message.content)
engine.runAndWait()