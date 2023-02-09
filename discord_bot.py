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
                    message = message.clean_content
                    image_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    if message == '':
                        message = f"{author}: 傳送了圖片"
                    else:
                        message = f"{author}: {message}(圖片)"
                    line_notify.send_image_message(sub_num, message, image_file_path)
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
                    message = message.clean_content
                    send_to_line_bot('video', sub_num, author, message, video_url=attachment.url,
                                     thumbnail_url=thumbnail_url)
                if attachment.filename.endswith(('m4a', '.wav', '.mp3', 'wav', 'aac', 'flac', 'ogg',
                                                 'opus')):
                    audio_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    if not attachment.filename.endswith('.m4a'):
                        audio_file_path = utils.convert_audio_to_m4a(audio_file_path)
                    audio_duration = utils.get_audio_duration(audio_file_path)
                    author = message.author.display_name
                    message = message.clean_content
                    send_to_line_bot('audio', sub_num, author, message, audio_url=attachment.url,
                                     audio_duration=audio_duration)
                else:
                    # TODO(LD): Handle other file types.
                    pass
        else:
            author = message.author.display_name
            message = message.clean_content
            line_notify.send_message(sub_num, f"{author}: {message}")


def send_to_line_bot(msg_type, sub_num, author, message, video_url=None, thumbnail_url=None,
                     audio_url=None, audio_duration=None):
    """Send message to line bot.

    Use zmq to send messages to line bot.

    :param msg_type: Message type, can be 'video', 'audio'.
    :param sub_num: Subscription number.
    :param author: Author of the message.
    :param message: Message content.
    :param video_url: Video url.
    :param thumbnail_url: Thumbnail url.
    :param audio_url: Audio url.
    :param audio_duration: Audio duration.
    """
    data = {'msg_type': msg_type, 'sub_num': sub_num, 'author': author, 'message': message}
    if msg_type == 'video':
        data['video_url'] = video_url
        data['thumbnail_url'] = thumbnail_url
    if msg_type == 'audio':
        data['audio_url'] = audio_url
        data['audio_duration'] = audio_duration
    json_data = json.dumps(data, ensure_ascii=False)
    for i in range(2):
        if i == 1:
            socket.send_json(json_data)
        time.sleep(1)


client.run(config.get('discord_bot_token'))
