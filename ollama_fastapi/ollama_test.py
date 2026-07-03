from ollama import Client

client = Client(
  host='192.168.0.10:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='gemma:2b', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])

print(response.message.content)