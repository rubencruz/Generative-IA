from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=openai_key)

response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[
        {'role':'user','content':'Hey There'}
    ]
)

print(response.choices[0].message.content)