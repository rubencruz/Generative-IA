from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv('GOOGLE_API_KEY')

client = genai.Client(api_key=gemini_key)

response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents='Explain how AI works in few words'
)

print(response.text)