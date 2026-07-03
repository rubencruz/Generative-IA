#chain of thought promting

from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv('GOOGLE_API_KEY')

client = OpenAI(
    api_key=gemini_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/'    
)

SYSTEM_PROMPT='''
You're an expert assistant in resolving user queries using chain of thought.
you work on START, PLAN and OUTPUT steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.

Rules:
- Strictly follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can
be multiple times) and finally OUTPUT(which is going to the displayed to user).

Output JSON format:
{'step':'START'|'PLAN'|'OUTPUT', 'content':'string'}

Example:
START: Hey, can you solve 2+3*5/10
PLAN:{'step':'PLAN, 'content':'Seems like user is interested in math problem'}
PLAN:{'step':'PLAN, 'content':'looking at the problem, we should solve this using BODMAS methods'}
PLAN:{'step':'PLAN, 'content':'yes, BODMAS is the correct thing to be done here'}
PLAN:{'step':'PLAN, 'content':'first we must multiply 3*5 which is 15'}
PLAN:{'step':'PLAN, 'content':'Now the new equation is 2+15/10}
PLAN:{'step':'PLAN, 'content':'we must perfom divide 15/10 = 1.5}
PLAN:{'step':'PLAN, 'content':'now the new equation is 2+1.5}
PLAN:{'step':'PLAN, 'content':'now finally lets perform addtion 2+1.5 = 3.5'}
PLAN:{'step':'PLAN, 'content':'great, we have solved and finally left with 3.5 as answer'}
OUTPUT:{'step':'OUTPUT, 'content':'3.5'}
'''


response = client.chat.completions.create(
    model='gemini-2.5-flash',
    response_format={'type':'json_object'},
    messages=[
        {'role':'system','content':SYSTEM_PROMPT},       
        {'role':'user','content':'Hey, write  a code to add n numbers in js'},
        {'role':'assistant','content':json.dumps(
            {"step":"START", "content":"The user wants a JavaScript code snippet to add 'n' numbers."}
            )
        }
    ]
)

print(response.choices[0].message.content)