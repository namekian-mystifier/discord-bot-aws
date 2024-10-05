# Get SSM parameters first
import boto3
import os
import config
import datetime
import discord
import logging
from discord import app_commands
from g4f.client import Client

REGION = os.environ["SSM_REGION"]
SSM_PARAM_NAME = os.environ["SSM_PARAM_NAME"]

ssm_client = boto3.client('ssm', region_name=REGION)
parameter_json = ssm_client.get_parameter(Name=SSM_PARAM_NAME)
settings_list = ["Parameter"]["Value"].split(",")

config.GUILD_ID = int(settings_list[0])
config.DISCORD_TOKEN = str(settings_list[1])
config.MAXIMUM_QUERY_SIZE = int(settings_list[2])
config.PROVIDER = str(settings_list[3])
config.LLM_MODEL = str(settings_list[4])
INPUT_MESSAGE_LIMIT = int(settings_list[5])

# import the llm wrapper after settings parameters
from openai_wrapper import summarize_chat_log

# we logging
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# restricting permissions
intents = discord.Intents.default()
intents.message_content = True

# setup for discord slash commands
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


def process_hours_to_timedelta(hours: int) -> datetime.timedelta:
    # deal with edge cases
    if hours < 1:
        hours = 1
    if hours > 24:
        hours = 24
    hours_timedelta = datetime.timedelta(hours=hours)
    # if first time retrieving, retrieve the full requested time
    if config.LAST_ACCESSED is None:
        config.LAST_ACCESSED = datetime.datetime.now()
        return hours_timedelta
    elapsed_time = datetime.datetime.now() - config.LAST_ACCESSED
    # shorten the summary for the sake of rate limits
    if elapsed_time < hours_timedelta:
        hours_timedelta = elapsed_time
    # log bot access
    config.LAST_ACCESSED = datetime.datetime.now()
    return hours_timedelta

# test command to check app status
@tree.command(
    name="basedgreeting",
    description="Receive a based greeting",
    guild=discord.Object(id=config.GUILD_ID)
)
async def basedgreeting(interaction):
    await interaction.response.send_message("Hello!")

# the summary
@tree.command(
    name="summarize",
    description="Summarize last x hours where x is from 1 to 24",
    guild=discord.Object(id=config.GUILD_ID)
)
async def summarize(interaction: discord.Interaction, hours: int):
    # defer interaction (llm prompt takes a while)
    await interaction.response.defer(thinking=True)

    # shhh
    g4f_client = Client()
    
    # calculate the timestamp for the earliest message based on requested summary duration
    requested_duration = process_hours_to_timedelta(hours)
    current_time = datetime.datetime.now()
    cutoff_time = current_time - requested_duration
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
    response_message = f"Here is what happened:\n" + response_message
    print("Response message:", response_message)

    # Return the summary to Discord
    await interaction.followup.send(response_message[:config.DISCORD_MESSAGE_LIMIT])


# register actions with Discord
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=config.GUILD_ID))
    print("Ready!")

# we running
client.run(config.DISCORD_TOKEN)
