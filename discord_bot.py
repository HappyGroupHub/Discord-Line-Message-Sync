"""This python file will host discord bot."""
import json
import time

import discord
import zmq
from discord import File

import line_notify
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
    """Initialize discord bot."""
    print("Bot is ready.")


@client.event
async def on_message(message):
    """Handle message event."""
    if message.author == client.user:
        return
    if message.author.id in config.get('discord_webhook_bot_ids'):
        return
    if message.channel.id in config.get('subscribed_discord_channels'):
        sub_num = config.get('subscribed_discord_channels').index(message.channel.id) + 1
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith(('.jpg', '.png', '.jpeg')):
                    author = message.author.display_name
                    message = message.content
                    image_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    if message == '':
                        message = f"{author}: 傳送了圖片"
                    else:
                        message = f"{author}: {message}(圖片)"
                    line_notify.send_image_message(sub_num, f"{author}: {message}", image_file_path)
                if attachment.filename.endswith('.mp4'):
                    video_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    thumbnail_path = utils.generate_thumbnail(video_file_path)

                    # Send thumbnail to discord, get url, and delete the message.
                    thumbnail_message = await message.channel.send(thumbnail_path,
                                                                   file=File(thumbnail_path))
                    thumbnail_url = thumbnail_message.attachments[0].url
                    await thumbnail_message.delete()

                    author = message.author.display_name
                    message = message.content
                    data = {'type': 'video', 'sub_num': sub_num, 'author': author,
                            'message': message,
                            'video_url': attachment.url,
                            'thumbnail_url': thumbnail_url}
                    json_data = json.dumps(data, ensure_ascii=False)
                    for i in range(2):
                        if i == 1:
                            socket.send_json(json_data)
                        time.sleep(1)
                else:
                    # TODO(LD): Handle other file types.
                    pass
        else:
            author = message.author.display_name
            message = message.content
            line_notify.send_message(sub_num, f"{author}: {message}")


client.run(config.get('discord_bot_token'))
