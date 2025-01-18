import pyttsx3

def tts(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()