from fastapi import FastAPI,Body
from ollama import Client
import json

app = FastAPI()
client = Client(
    host='192.168.0.10:11434',
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/contact-us")
def read_root():
    return {"email": "contact@gmail.com"}

@app.post("/chat")
def chat(message: str= Body(..., description='The message')):
    response = client.chat(model='gemma:2b',messages=[
        {'role':'user', 'content':message}
    ])
    return { 'response': response.message.content}