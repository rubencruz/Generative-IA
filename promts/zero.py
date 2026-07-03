from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv('GOOGLE_API_KEY')

client = OpenAI(
    api_key=gemini_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/'    
)

# Zero shot prompting: Directly giving the inst to the model
SYSTEM_PRONT = 'You should only anwwer the coding related questions. Do not aswer anything else.' \
'Your name is Alexa. If user ask something other than coding, just say sorry!'

response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {'role':'system','content':SYSTEM_PRONT},
        {'role':'user','content':'Hey I am Ruben, can you write a python code to translate the word hello to Spanish'}
    ]
)

print(response.choices[0].message.content)