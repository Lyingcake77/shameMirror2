from ollama import chat, Client
from ollama import ChatResponse

def ask_ollama(text):
    response: ChatResponse = chat(model='llama2-uncensored', messages=[
        {
            'role': 'user',
            'content': text,
        },
    ])
    return response.message.content
def ask_ollama_client(text):
    client = Client(
        host='http://192.168.0.153:11434'
    )
    response: ChatResponse = client.chat(model='llama2-uncensored', messages=[
        {
            'role': 'user',
            'content': text,
        },
    ])
    return response.message.content

def generate_shame(description, useClient=False, reverse_shame = False):
    llm_shaming_prompt = 'Generate an insult based on the following criteria: '
    if reverse_shame:
        llm_shaming_prompt = 'Generate Compliments based on the following criteria: '
    if useClient:
        return ask_ollama_client(llm_shaming_prompt+description)
    else:
        return ask_ollama(llm_shaming_prompt+description)

