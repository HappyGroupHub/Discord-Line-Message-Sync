"""This python file will host discord bot."""
import json
import time

import discord
import zmq

import utilities as utils

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

config = utils.read_config()


@client.event
async def on_ready():
    print("Bot is ready.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id == int(config.get('discord_channel_id')):
        author = message.author.display_name
        message = message.content
        data = {'author': author, 'message': message}
        json_data = json.dumps(data, ensure_ascii=False)
        for i in range(2):
            if i == 1:
                socket.send_json(json_data)
            time.sleep(1)


client.run(config.get('discord_bot_token'))
