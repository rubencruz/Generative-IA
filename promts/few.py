from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv('GOOGLE_API_KEY')

client = OpenAI(
    api_key=gemini_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/'    
)

# few shot prompting: Directly giving the inst to the model and few examples to the moel
SYSTEM_PROMPT = 'You should only anwwer the coding related questions. Do not aswer anything else.' \
'Your name is Alexa. If user ask something other than coding, just say sorry!' \
'Examples:' \
'Q: can you explain the a+b whole square' \
'A: Sorry, I can only help with coding related question'

response = client.chat.completions.create(
    model='gemini-2.5-flash',
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},
        {'role':'user','content':'Hey I am Ruben, can you solve (a+b)(a-b)'}
    ]
)

print(response.choices[0].message.content)