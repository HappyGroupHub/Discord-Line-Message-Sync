"""This python file will host discord bot."""

import discord

import utilities as utils

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Bot is ready.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!hello"):
        await message.channel.send("Hello!")


client.run(utils.read_config().get('discord_bot_token'))
