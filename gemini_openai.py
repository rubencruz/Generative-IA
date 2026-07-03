from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key= os.getenv('GOOGLE_API_KEY')

client = OpenAI(
    api_key=gemini_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/'    
)

response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {'role':'system','content':'You are and expert in naths and only answer math releted questions, that if they query is not related to maths, then just say sorry and do not answer that!'},
        {'role':'user','content':'Hey I am Ruben, can you code a python program that can print hello'}
    ]
)

print(f'>>>: {response.choices[0].message.content}')