"""This python file will host discord bot."""
import json
import time

import discord
import zmq
from discord import File
from discord import app_commands
from discord.ext import commands

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


@client.tree.command(name="link", description="此指令用來與Line群組進行綁定, 並同步訊息")
@app_commands.describe(binding_code="輸入你的綁定碼")
async def link(interaction: discord.Interaction, binding_code: str):
    binding_info = utils.get_binding_code_info(binding_code)
    if not binding_info:
        reply_message = "綁定失敗, 該綁定碼輸入錯誤或格式不正確, 請再試一次."
        await interaction.response.send_message(reply_message, ephemeral=True)
    elif binding_info['expiration'] < time.time():
        utils.remove_binding_code(binding_code)
        reply_message = "綁定失敗, 此綁定碼已逾5分鐘內無使用而過期, 請重新於Line群組內輸入: `!綁定`"
        await interaction.response.send_message(reply_message, ephemeral=True)
    else:
        webhook = await interaction.channel.create_webhook(name="Line訊息同步")
        utils.add_new_sync_channel(binding_info['line_group_id'], binding_info['line_group_name'],
                                   binding_info['line_notify_token'], str(interaction.channel.id),
                                   interaction.channel.name, webhook.url)
        utils.remove_binding_code(binding_code)
        push_message = f"綁定成功！\n" \
                       f"     ----------------------\n" \
                       f"    |    Discord <> Line   |\n" \
                       f"    |    訊息同步機器人   |\n" \
                       f"     ----------------------\n\n" \
                       f"Discord頻道：{interaction.channel.name}\n" \
                       f"Line群組      ：{binding_info['line_group_name']}\n" \
                       f"===================\n" \
                       f"目前支援同步：文字訊息、圖片、影片、音訊"
        reply_message = f"**【Discord <> Line 訊息同步機器人 - 綁定成功！】**\n\n" \
                        f"Discord頻道：{interaction.channel.name}\n" \
                        f"Line群組      ：{binding_info['line_group_name']}\n" \
                        f"========================================\n" \
                        f"目前支援同步：文字訊息、圖片、影片、音訊"
        line_notify.send_message(push_message, binding_info['line_notify_token'])
        await interaction.response.send_message(reply_message)


@client.tree.command(name="unlink", description="此指令用來解除與Line群組的綁定, 並取消訊息同步")
@app_commands.describe()
async def unlink(interaction: discord.Interaction):
    channel_id = str(interaction.channel.id)
    subscribed_info = utils.get_subscribed_info_by_discord_channel_id(channel_id)
    if not subscribed_info:
        reply_message = "此頻道並未綁定任何Line群組！"
        await interaction.response.send_message(reply_message, ephemeral=True)
    else:
        reply_message = f"**【Discord <> Line 訊息同步機器人 - 解除同步！】**\n\n" \
                        f"Discord頻道：{subscribed_info['discord_channel_name']}\n" \
                        f"Line群組      ：{subscribed_info['line_group_name']}\n" \
                        f"========================================\n" \
                        f"請問確定要解除同步嗎？"
        await interaction.response.send_message(reply_message,
                                                view=UnlinkConfirmation(subscribed_info),
                                                ephemeral=True)


class UnlinkConfirmation(discord.ui.View):
    def __init__(self, subscribed_info):
        super().__init__(timeout=20)
        self.subscribed_info = subscribed_info

    @discord.ui.button(label="⛓️ 確認解除同步", style=discord.ButtonStyle.danger)
    async def unlink_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        utils.remove_sync_channel_by_discord_channel_id(self.subscribed_info['discord_channel_id'])
        push_message = f"已解除同步！\n" \
                       f"     ----------------------\n" \
                       f"    |    Discord <> Line   |\n" \
                       f"    |    訊息同步機器人   |\n" \
                       f"     ----------------------\n\n" \
                       f"Discord頻道：{self.subscribed_info['discord_channel_name']}\n" \
                       f"Line群組      ：{self.subscribed_info['line_group_name']}\n" \
                       f"===================\n" \
                       f"執行者：{interaction.user.display_name}\n"
        reply_message = f"**【Discord <> Line 訊息同步機器人 - 已解除同步！】**\n\n" \
                        f"Discord頻道：{self.subscribed_info['discord_channel_name']}\n" \
                        f"Line群組      ：{self.subscribed_info['line_group_name']}\n" \
                        f"========================================\n" \
                        f"執行者：{interaction.user.display_name}\n"
        self.stop()
        line_notify.send_message(push_message, self.subscribed_info['line_notify_token'])
        await interaction.response.send_message(reply_message)

    @discord.ui.button(label="取消操作", style=discord.ButtonStyle.primary)
    async def unlink_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        reply_message = "操作已取消！"
        self.stop()
        await interaction.response.send_message(reply_message, ephemeral=True)


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
                    image_file_path = utils.download_file_from_url(subscribed_info['folder_name'],
                                                                   attachment.url,
                                                                   attachment.filename)
                    if message == '':
                        message = f"{author}: 傳送了圖片"
                    else:
                        message = f"{author}: {message}(圖片)"
                    line_notify.send_image_message(message, image_file_path,
                                                   subscribed_info['line_notify_token'])
                if attachment.filename.endswith(supported_video_format):
                    video_file_path = utils.download_file_from_url(subscribed_info['folder_name'],
                                                                   attachment.url,
                                                                   attachment.filename)
                    thumbnail_path = utils.generate_thumbnail(video_file_path)

                    # Send thumbnail to discord, get url, and delete the message.
                    thumbnail_message = await message.channel.send(thumbnail_path,
                                                                   file=File(thumbnail_path))
                    thumbnail_url = thumbnail_message.attachments[0].url
                    await thumbnail_message.delete()

                    message = message.clean_content
                    send_to_line_bot('video', sub_num, author, message,
                                     video_url=attachment.url, thumbnail_url=thumbnail_url)
                if attachment.filename.endswith(supported_audio_format):
                    audio_file_path = utils.download_file_from_url(sub_num, attachment.url,
                                                                   attachment.filename)
                    if not attachment.filename.endswith('.m4a'):
                        audio_file_path = utils.convert_audio_to_m4a(audio_file_path)
                    audio_duration = utils.get_audio_duration(audio_file_path)
                    message = message.clean_content
                    send_to_line_bot('audio', sub_num, author, message,
                                     audio_url=attachment.url, audio_duration=audio_duration)
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
