from g4f.client import Client
from g4f import Provider
import config

# the query and max prompt size
selected_provider = getattr(Provider, config.PROVIDER)


# shh
def summarize_chat_log(client: Client, chat_log: str) -> str:
    query = config.SUMMARIZE_QUERY % chat_log[-config.MAXIMUM_QUERY_SIZE+len(config.SUMMARIZE_QUERY):]
    response = client.chat.completions.create(
        model=config.LLM_MODEL,
        provider=selected_provider,
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content
