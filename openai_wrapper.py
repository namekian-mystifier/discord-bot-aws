from g4f.client import Client
from g4f import Provider
import os

# the query and max prompt size
SUMMARIZE_QUERY = "Hello! Can you summarize the discord chat between members of a wow guild discord between {[%s]} in max 1900 characters and using bullet points for the main topics and get straight to the summary with no intro?"
MAXIMUM_QUERY_SIZE = os.environ["MAXIMUM_LLM_QUERY_LEN"]
PROVIDER = os.environ["LLM_PROVIDER"]
LLM_MODEL = os.environ["LLM_MODEL"]

selected_provider = getattr(Provider, PROVIDER)


# shh
def summarize_chat_log(client: Client, chat_log: str) -> str:
    query = SUMMARIZE_QUERY % chat_log[-MAXIMUM_QUERY_SIZE+len(SUMMARIZE_QUERY):]
    response = client.chat.completions.create(
        model=LLM_MODEL,
        provider=selected_provider,
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content
