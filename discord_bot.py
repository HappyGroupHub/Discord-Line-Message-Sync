"""This python file will host discord bot."""

import discord

import line_notify
import utilities as utils

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

config = utils.read_config()


@client.event
async def on_ready():
    print("Bot is ready.")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.id == utils.get_discord_webhook_id():
        return
    if message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith(('.jpg', '.png', '.jpeg')):
                author = message.author.display_name
                message = message.content
                image_file_path = utils.download_file_from_url(attachment.url, attachment.filename)
                line_notify.send_image_message(f"{author}: {message}", image_file_path)
            else:
                line_notify.send_message(message.content)
    elif message.channel.id == int(config.get('discord_channel_id')):
        author = message.author.display_name
        message = message.content
        line_notify.send_message(f"{author}: {message}")


client.run(config.get('discord_bot_token'))
