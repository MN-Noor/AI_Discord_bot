import os

# Load environment variables

def roadmap(query):
    import os
    openai_key =os.environ["pathopen"]
    assistant_id =os.environ["pathassist"]
    from openai import OpenAI

    # Initialize OpenAI client
    client = OpenAI(api_key=openai_key)

    # Create a new thread
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=query,
    )


    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant_id,
    )

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(messages)
    else:
        print(run.status)

    tool_outputs = []
  # Loop through each tool in the required action section
    try:
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "fetch_google_results":
                tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": "proper roadmap"
                })
    except AttributeError:
        print("Error: Unable to access tool calls.")


    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )
            print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
        print(messages)
        return(messages.data[0].content[0].text.value)
    else:
        print(run.status)


def fetch_google_results(query):
    import os
    import http.client
    import urllib.parse
    import json
    num_results = 2
    conn = http.client.HTTPSConnection("api.hasdata.com")

    headers = {
        'x-api-key':os.environ["googleSearch"] ,
        'Content-Type': "application/json"
    }

    # Encode the query and replace spaces with '+'
    encoded_query = urllib.parse.quote_plus(query)

    # Construct the URL with the desired number of results
    url = f"/scrape/google/serp?q={encoded_query}&location=Austin%2CTexas%2CUnited+States&deviceType=desktop&num={num_results}"

    conn.request("GET", url, headers=headers)

    res = conn.getresponse()
    data = res.read()
    response_data = json.loads(data.decode("utf-8"))

    result_string = ""

    if 'organicResults' in response_data:
        for result in response_data['organicResults']:
            result_string += f"Title: {result.get('title', '')}\nLink: {result.get('link', '')}\nSource: {result.get('source', '')}\n\n"

    return result_string





# if __name__ == '__main__':
#     show()