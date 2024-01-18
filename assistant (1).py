
#pip install openai

import openai
from openai import OpenAI

client = OpenAI(api_key='OPENAI-API-KEY')

file = client.files.create(
    file=open('Data/PythonMastery.pdf','rb'),
    purpose="assistants"
)

assistant = client.beta.assistants.create(
    name='Python developer',
    instructions='You are a python developer. Give the script for the instructions I give you and answer the questions from the pdf file.',
    tools=[{"type":"code_interpreter"}],
    model='gpt-3.5-turbo-1106',
    file_ids=[file.id]
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role='user',
    content='How do you use the abstract data classes from abc  library? Give example.'
)

thread_messages = client.beta.threads.messages.list(thread.id)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id = assistant.id
)

run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
)

while True:
  run = client.beta.threads.runs.retrieve(
    thread_id=thread.id,
    run_id=run.id
  )

  if run.status=='completed':
    messages = client.beta.threads.messages.list(thread.id)
    current_message = messages.data[0]
    print(current_message.content[0].text.value)
    break
