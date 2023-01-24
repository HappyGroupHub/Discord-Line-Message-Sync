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
                    image_file_path = utils.download_file_from_url(attachment.url,
                                                                   attachment.filename)
                    line_notify.send_image_message(sub_num, f"{author}: {message}", image_file_path)
                else:
                    # TODO(LD): Handle other file types.
                    pass
        else:
            author = message.author.display_name
            message = message.content
            line_notify.send_message(sub_num, f"{author}: {message}")


client.run(config.get('discord_bot_token'))
