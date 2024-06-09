
from openai import OpenAI
import time

def create_thread(client):
    thread = client.beta.threads.create()
    return thread.id

def get_response(client, thread_id, assistant_id, content):
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages.data[0].content[0].text.value

def check_code(query):
    import os
    openai_api=os.environ["codeapi"]
    assistant_id=os.environ["codeassist"]
    client = OpenAI(api_key=openai_api)
    thread_id = create_thread(client)
    messages = get_response(client, thread_id, assistant_id,query)
    print(messages)
    return messages

