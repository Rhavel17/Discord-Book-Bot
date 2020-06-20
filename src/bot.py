import os
from dotenv import load_dotenv
import discord

# Load environment variable(s) from .env file to shell's environment variables
load_dotenv()

# Get the value of the 'DISCORD_TOKEN' env variable
TOKEN = os.getenv('DISCORD_TOKEN')

# Create instance of Client (represents client connection to Discord)
client = discord.Client()

# Called when 'client is done preparing the data received from discord
# Usually after login is successful and the Client.guilds are filled up'
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

# Run the Client
client.run(TOKEN)
