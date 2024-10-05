import datetime
import discord
import logging
from discord import app_commands
import os
from g4f.client import Client
from openai_wrapper import summarize_chat_log

# we logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# environment setup
GUILD_ID = os.environ["GUILDID"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
DISCORD_MESSAGE_LIMIT = 2000
INPUT_MESSAGE_LIMIT = os.environ["INPUT_MESSAGE_LIMIT"]

# restricting permissions
intents = discord.Intents.default()
intents.message_content = True

# setup for discord slash commands
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# test command to check app status
@tree.command(
    name="basedgreeting",
    description="Receive a based greeting",
    guild=discord.Object(id=GUILD_ID)
)
async def basedgreeting(interaction):
    await interaction.response.send_message("Hello!")

# the summary
@tree.command(
    name="summarize",
    description="Summarize last x hours where x is from 1 to 24",
    guild=discord.Object(id=GUILD_ID)
)
async def summarize(interaction: discord.Interaction, hours: int):
    # defer interaction (llm prompt takes a while)
    await interaction.response.defer(thinking=True)
    
    # shhh
    g4f_client = Client()
    
    # calculate the timestamp for the earliest message based on requested summary duration
    current_time = datetime.datetime.now()
    cutoff_time = current_time - datetime.timedelta(hours=hours)
    print("Cuttoff time:", str(cutoff_time))

    # Assemble the chat log
    messages = [message async for message in interaction.channel.history(after=cutoff_time)]
    chat_log = ''
    for message in messages:
        if len(message.content) > INPUT_MESSAGE_LIMIT:
            proc_message = message.content[:INPUT_MESSAGE_LIMIT]
        else:
            proc_message = message.content
        chat_log += f'''
{message.author.display_name}:
{proc_message}
'''
    print("Chat log size: ", len(chat_log))

    # Prompt the thing
    response_message = summarize_chat_log(g4f_client, chat_log)
    response_message = f"Here is a summary of the past {hours} hours:\n" + response_message
    print("Response message:", response_message)

    # Return the summary to Discord
    await interaction.followup.send(response_message[:DISCORD_MESSAGE_LIMIT])


# register actions with Discord
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")

# we running
client.run(DISCORD_TOKEN)
