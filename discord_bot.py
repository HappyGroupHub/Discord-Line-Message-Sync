"""This python file will host discord bot."""
import json
import time

import discord
from discord import File
from discord import app_commands
from discord.ext import commands
import zmq


import line_notify
import utilities as utils

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

supported_image_format = ('.jpg', '.png', '.jpeg')
supported_video_format = '.mp4'
supported_audio_format = ('.m4a', '.wav', '.mp3', '.aac', '.flac', '.ogg', '.opus')

config = utils.read_config()


@client.event
async def on_ready():
    """Initialize discord bot."""
    print("Bot is ready.")
    try:
        synced = await client.tree.sync()
        print(f"Synced {synced} commands.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@client.tree.command(name="link")
@app_commands.describe(binding_code="輸入你的綁定碼")
async def link(interaction: discord.Interaction, binding_code: str):
    binding_info = utils.get_binding_code_info(binding_code)
    if not binding_info:
        reply_message = "綁定碼錯誤，請重新輸入..."
    elif binding_info['expiration'] < time.time():
        reply_message = "綁定碼已過期, 請重新於Line群組內輸入: !綁定"
    else:
        webhook = await interaction.channel.create_webhook(name="Line訊息同步")
        utils.add_new_sync_channel(binding_info['line_group_id'], binding_info['line_notify_token'],
                                   str(interaction.channel.id), webhook.url)
        reply_message = "綁定成功！"
    await interaction.response.send_message(reply_message)


@client.event
async def on_message(message):
    """Handle message event."""
    if message.author == client.user:
        return
    discord_webhook_bot_ids = utils.get_discord_webhook_bot_ids()
    if message.author.id in discord_webhook_bot_ids:
        return
    subscribed_discord_channels = utils.get_subscribed_discord_channels()
    if message.channel.id in subscribed_discord_channels:
        subscribed_info = utils.get_subscribed_info_by_discord_channel_id(str(message.channel.id))
        sub_num = subscribed_info['sub_num']
        author = message.author.display_name
        if message.attachments:
            for attachment in message.attachments:
                if attachment.filename.endswith(supported_image_format):
                    message = message.clean_content
                    image_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    if message == '':
                        message = f"{author}: 傳送了圖片"
                    else:
                        message = f"{author}: {message}(圖片)"
                    line_notify.send_image_message(message, image_file_path,
                                                   subscribed_info['line_notify_token'])
                if attachment.filename.endswith(supported_video_format):
                    video_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    thumbnail_path = utils.generate_thumbnail(video_file_path)

                    # Send thumbnail to discord, get url, and delete the message.
                    thumbnail_message = await message.channel.send(thumbnail_path,
                                                                   file=File(thumbnail_path))
                    thumbnail_url = thumbnail_message.attachments[0].url
                    await thumbnail_message.delete()

                    message = message.clean_content
                    send_to_line_bot('video', sub_num, author, message, video_url=attachment.url,
                                     thumbnail_url=thumbnail_url)
                if attachment.filename.endswith(supported_audio_format):
                    audio_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    if not attachment.filename.endswith('.m4a'):
                        audio_file_path = utils.convert_audio_to_m4a(audio_file_path)
                    audio_duration = utils.get_audio_duration(audio_file_path)
                    message = message.clean_content
                    send_to_line_bot('audio', sub_num, author, message, audio_url=attachment.url,
                                     audio_duration=audio_duration)
                else:
                    # TODO(LD): Handle other file types.
                    pass
        else:
            message = message.clean_content
            line_notify.send_message(f"{author}: {message}", subscribed_info['line_notify_token'])


def send_to_line_bot(msg_type, sub_num, author, message, video_url=None, thumbnail_url=None,
                     audio_url=None, audio_duration=None):
    """Send message to line bot.

    Use zmq to send messages to line bot.

    :param msg_type: Message type, can be 'video', 'audio'.
    :param sub_num: Subscribed sync channels num.
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
