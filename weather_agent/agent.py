#chain of thought promting

from openai import OpenAI
#from ai_keys import gemini_key
from pydantic import BaseModel, Field
from typing import Optional
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()
gemini_key = os.getenv('GOOGLE_API_KEY')

class MyOutputFormat(BaseModel):
    step: str = Field(..., description='')
    content: Optional[str] = Field(None,description='')
    tool: Optional[str] = Field(None,description='')
    input: Optional[str] = Field(None,description='')


client = OpenAI(
    api_key=gemini_key,
    base_url='https://generativelanguage.googleapis.com/v1beta/'    
)

def get_weather(city:str):
    url = f'https://wttr.in/{city.lower()}?format=%C+%t'
    response  = requests.get(url)

    if response.status_code == 200:
        return f'The weather in {city} is {response.text}'
    return 'Something went wrong'

available_tools = {
    'get_weather':get_weather
}

SYSTEM_PROMPT='''
You're an expert assistant in resolving user queries using chain of thought.
you work on START, PLAN and OUTPUT steps.
Once you think enough PLAN has been done, finally you can give an OUTPUT.
You can also call a tool if required from the list of available tools
For every tool call wait for the observe step which is the output from the called tool.

Rules:
- Strictly follow the given JSON output format
- Only run one step at a time.
- The sequence of steps is START (where user gives an input), PLAN (That can
be multiple times) and finally OUTPUT(which is going to the displayed to user).

Output JSON format:
{'step':'START'|'PLAN'|'OUTPUT'|'TOOL', 'content':'string', 'tool':'string','input'|'output':'string'}

Availabel tools:
- get_weather: takes city name as an input string and returns the weather info about the city.

Example 1:
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

Example 2:
START: what is the weather of Delhi?
PLAN:{'step':'PLAN, 'content':'Seems like user is interested in getting weather of Delhi in India'}
PLAN:{'step':'PLAN, 'content':'Lets see if we have any available tool from the list of available tools'}
PLAN:{'step':'PLAN, 'content':'Great, we have get_weather tool available for this query'}
PLAN:{'step':'PLAN, 'content':'I need to call get_weather tool for Delhi as input for city'}
PLAN:{'step':'TOOL':'tool':get_weather, 'input':'Delhi'}
PLAN:{'step':'OBSERVE':'tool':get_weather, 'output':'The temperature of Delhi is cloudy with 20 C'}
PLAN:{'step':'PLAN, 'content':'Great, I got the weather info about Delhi'}
OUTPUT:{'step':'OUTPUT, 'content':'The current weather in Delhi is 20 C with soume cloudy sky'}
'''

print('\n\n')

message_history = [
    {'role':'system','content':SYSTEM_PROMPT},
]

user_query = input('input: ')
message_history.append({'role':'user','content':user_query})

while True:
    response = client.chat.completions.parse(
        model='gemini-2.5-flash',
        #model='gpt-4o',
        response_format=MyOutputFormat,
        messages=  message_history
    )

    raw_result = response.choices[0].message.content
    message_history.append({'role':'assistant','content':raw_result})

    parsed_result = response.choices[0].message.parsed
    
    if parsed_result.step == 'START':
        print('-> ',parsed_result.content)
        continue

    if parsed_result.step == 'TOOL':
        tool_to_call = parsed_result.tool
        tool_input = parsed_result.input
        print(f'Tool -> *  {tool_to_call}({tool_input})')

        tool_response = available_tools[tool_to_call](tool_input)
        print(f'Tool -> *  {tool_to_call}({tool_input}) = {tool_response}')
        message_history.append({'role':'developer','content':json.dumps(
            {'step':'OBSERVE','tool':tool_to_call,'input':tool_input,'output':tool_response}
        ) })
        continue

    if parsed_result.step == 'PLAN':
        print('-> * ',parsed_result.content)
        continue

    if parsed_result.step == 'OUTPUT':
        print('* <-> * ',parsed_result.content)
        break

print('\n\n')