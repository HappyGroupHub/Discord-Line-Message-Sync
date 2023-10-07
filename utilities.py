"""This python file will handle some extra functions."""
import datetime
import json
import os
import random
import subprocess
import sys
import time
from os.path import exists

import requests
import yaml
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# ++--------------------------------++
# | Discord-Line-Message-Sync v0.2.0 |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# Paste your endpoint for the webhook here.
# You can use ngrok to get a free static endpoint now!
# Find out more here: https://ngrok.com/
webhook_url: ''

# Bot tokens and secrets
# You will need to fill in the tokens and secrets for your Line, Line Notify and Discord bots
# Line bot: https://developers.line.biz/console/
# Line Notify: https://notify-bot.line.me/my/services/
# Discord bot: https://discord.com/developers/applications/
Line_bot:
  channel_access_token: ''
  channel_secret: ''
Line_notify:
  client_id: ''
  client_secret: ''
Discord_bot:
  bot_token: ''
"""
                )
    sys.exit()


def read_config():
    """Read config file.

    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.

    :rtype: dict
    """
    if not exists('./config.yml'):
        print("Config file not found, create one by default.\nPlease finish filling config.yml")
        with open('config.yml', 'w', encoding="utf8"):
            config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            config = {
                'webhook_url': data['webhook_url'],
                'line_channel_secret': data['Line_bot']['channel_secret'],
                'line_channel_access_token': data['Line_bot']['channel_access_token'],
                'line_notify_id': data['Line_notify']['client_id'],
                'line_notify_secret': data['Line_notify']['client_secret'],
                'discord_bot_token': data['Discord_bot']['bot_token']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def get_subscribed_discord_channels():
    """Get subscribed discord channels.

    :return list: Subscribed discord channels.
    """
    if not exists('./sync_channels.json'):
        print("sync_channels.json not found, create one by default.")
        with open('sync_channels.json', 'w', encoding="utf8") as file:
            json.dump([], file, indent=4)
            file.close()
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    subscribed_discord_channels = [int(entry['discord_channel_id']) for entry in data]
    return subscribed_discord_channels


def get_subscribed_line_channels():
    if not exists('./sync_channels.json'):
        print("sync_channels.json not found, create one by default.")
        with open('sync_channels.json', 'w', encoding="utf8") as file:
            json.dump([], file, indent=4)
            file.close()
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    subscribed_line_channels = [entry['line_group_id'] for entry in data]
    return subscribed_line_channels


def get_subscribed_info_by_discord_channel_id(discord_channel_id):
    """Get subscribed info by discord channel id.

    :param int discord_channel_id: Discord channel id.
    :return dict: Subscribed info. Include line_group_id, line_notify_token, discord_channel_id,
    discord_channel_webhook and sub_num.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    for index, entry in enumerate(data):
        if entry['discord_channel_id'] == discord_channel_id:
            subscribed_info = entry.copy()
            return subscribed_info
    return {}


def get_subscribed_info_by_line_group_id(line_group_id):
    """Get subscribed info by line group id.

    :param str line_group_id: Line group id.
    :return dict: Subscribed info. Include line_group_id, line_notify_token, discord_channel_id,
    discord_channel_webhook and sub_num.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    for index, entry in enumerate(data):
        if entry['line_group_id'] == line_group_id:
            subscribed_info = entry.copy()
            return subscribed_info
    return {}


def get_subscribed_info_by_sub_num(sub_num):
    """Get subscribed info by sub num.

    :param int sub_num: Subscribed sync channels num.
    :return dict: Subscribed info. Include line_group_id, line_notify_token, discord_channel_id,
    discord_channel_webhook and sub_num.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    for index, entry in enumerate(data):
        if entry['sub_num'] == sub_num:
            subscribed_info = entry.copy()
            return subscribed_info
    return {}


def add_new_sync_channel(line_group_id, line_group_name, line_notify_token,
                         discord_channel_id, discord_channel_name, discord_channel_webhook):
    """Add new sync channel.

    :param str line_group_id: Line group id.
    :param str line_group_name: Line group name.
    :param str line_notify_token: Line notify token.
    :param int discord_channel_id: Discord channel id.
    :param str discord_channel_name: Discord channel name.
    :param str discord_channel_webhook: Discord channel webhook.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    if not data:
        sub_num = 1
    else:
        max_dict = max(data, key=lambda x: x.get('sub_num', 0))
        sub_num = max_dict.get('sub_num', 0) + 1
    folder_name = f'{line_group_name}_{discord_channel_name}'
    data.append({
        'sub_num': sub_num,
        'folder_name': folder_name,
        'line_group_id': line_group_id,
        'line_group_name': line_group_name,
        'line_notify_token': line_notify_token,
        'discord_channel_id': discord_channel_id,
        'discord_channel_name': discord_channel_name,
        'discord_channel_webhook': discord_channel_webhook
    })
    update_json('sync_channels.json', data)


def remove_sync_channel_by_discord_channel_id(discord_channel_id):
    """Remove sync channel by discord channel id.

    :param int discord_channel_id: Discord channel id.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    for index, entry in enumerate(data):
        if entry['discord_channel_id'] == discord_channel_id:
            data.pop(index)
            update_json('sync_channels.json', data)


def get_discord_webhook_bot_ids():
    """Get discord webhook bot ids.

    :return list: Discord webhook bot ids.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    discord_channel_webhooks = [entry['discord_channel_webhook'] for entry in data]
    discord_webhook_bot_ids = [int(webhook.split('/')[-2]) for webhook in discord_channel_webhooks]
    return discord_webhook_bot_ids


def download_file_from_url(folder_name, url, filename):
    """Download file from url.

    Use to download any files from discord.

    :param str folder_name: Folder name of downloaded files.
    :param url: url of file
    :param filename: filename of file
    :return str: file path
    """
    r = requests.get(url, allow_redirects=True, timeout=5)
    path = f'./downloads/{folder_name}'
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = f'{path}/{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}_{filename}'
    with open(file_path, 'wb') as fd:
        fd.write(r.content)
    return file_path


def download_file_from_line(folder_name, source, message_type):
    """Get file binary and save them in PC.

    Use to download files from LINE.

    :param str folder_name: Folder name of downloaded files.
    :param source: source of file that given by LINE
    :param message_type: message type from line
    :return str: file path
    """
    file_type = {
        'image': 'jpg',
        'video': 'mp4',
        'audio': 'm4a',
    }
    path = f'./downloads/{folder_name}'
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = \
        f'{path}/{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}.{file_type.get(message_type)}'
    with open(file_path, 'wb') as fd:
        for chunk in source.iter_content():
            fd.write(chunk)
    return file_path


def generate_thumbnail(video_path, thumbnail_path=None, time=1):
    """Generate thumbnail from video.

    According to LINE API, when sending video, thumbnail is required.

    :param str video_path: Video path.
    :param str thumbnail_path: Thumbnail path. If not given, will use video path to generate.
    :param int time: Frame of video to generate thumbnail.(in seconds), default is 1.
    :return str: Thumbnail path.
    """
    if thumbnail_path is None:
        thumbnail_path = f'{os.path.splitext(video_path)[0]}.jpg'
    video = VideoFileClip(video_path)
    video.save_frame(thumbnail_path, t=time)
    return thumbnail_path


def convert_audio_to_m4a(audio_path, result_path=None):
    """Convert audio file to m4a format.

    According to LINE API, audio file must be m4a format.
    You must install ffmpeg to use this function.
    Support: mp3, wav, aac, flac, ogg, opus format.

    :param str audio_path: Audio path.
    :param result_path: Result path. If not given, will use audio path to generate.
    :return str: Audio path.
    """
    if result_path is None:
        result_path = f'{os.path.splitext(audio_path)[0]}.m4a'
    subprocess.run(
        f'ffmpeg -i {audio_path} -c:a aac -vn {result_path} -hide_banner -loglevel error')
    return result_path


def get_audio_duration(audio_path, file_format='m4a'):
    """Get audio duration.

    You must install ffmpeg to use this function.

    :param str audio_path: Audio path.
    :param str file_format: Audio file format. Default is m4a.
    :return int duration: Audio duration in milliseconds.
    """
    audio = AudioSegment.from_file(audio_path, format=file_format)
    duration = audio.duration_seconds * 1000
    return duration


def generate_binding_code(line_group_id, line_group_name, line_notify_token):
    """Generate binding code.

    :param str line_group_id: Line group id.
    :param str line_group_name: Line group name.
    :param str line_notify_token: Line notify token.
    :return str: Binding code.
    """
    if not os.path.exists('./binding_codes.json'):
        with open('binding_codes.json', 'w', encoding="utf8") as file:
            json.dump({}, file, indent=4)
            file.close()
    data = json.load(open('binding_codes.json', 'r', encoding="utf8"))
    binding_code = str(random.randint(100000, 999999))
    data[binding_code] = {'line_group_id': line_group_id, 'line_group_name': line_group_name,
                          'line_notify_token': line_notify_token, 'expiration': time.time() + 300}
    update_json('binding_codes.json', data)
    return binding_code


def remove_binding_code(binding_code):
    """Remove binding code from binding_codes.json.

    :param str binding_code: Binding code.
    """
    data = json.load(open('binding_codes.json', 'r', encoding="utf8"))
    if binding_code in data:
        data.pop(binding_code)
        update_json('binding_codes.json', data)


def get_binding_code_info(binding_code):
    """Get binding code info.

    :param str binding_code: Binding code.
    :return dict: Binding code info. Include line_group_id, line_notify_token and expiration.
    """
    data = json.load(open('binding_codes.json', 'r', encoding="utf8"))
    if binding_code in data:
        return data[binding_code]
    return {}


def update_json(file, data):
    """Update a json file.

    :param str file: The file to update.
    :param dict data: The data to update.
    """
    with open(file, 'w', encoding="utf8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        file.close()
