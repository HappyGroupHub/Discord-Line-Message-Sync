"""This python file will handle some extra functions."""
import datetime
import json
import os
import subprocess
import sys
from os.path import exists
from typing import List

import requests
import yaml
from moviepy.video.io.VideoFileClip import VideoFileClip
from pydub import AudioSegment
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""# ++--------------------------------++
# | Discord-Line-Message-Sync v0.1.6 |
# | Made by LD (MIT License)         |
# ++--------------------------------++

# Bot tokens and secrets
# You will need to fill in the tokens and secrets for both your Line and Discord bots
Line:
  channel_access_token: ''
  channel_secret: ''
Discord:
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
                'line_channel_secret': data['Line']['channel_secret'],
                'line_channel_access_token': data['Line']['channel_access_token'],
                'discord_bot_token': data['Discord']['bot_token']
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
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    subscribed_discord_channels = [int(entry['discord_channel_id']) for entry in data]
    return subscribed_discord_channels


def get_subscribed_line_channels():
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
            subscribed_info['sub_num'] = index + 1
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
            subscribed_info['sub_num'] = index + 1
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
        if index + 1 == sub_num:
            subscribed_info = entry.copy()
            subscribed_info['sub_num'] = index + 1
            return subscribed_info
    return {}


def get_discord_webhook_bot_ids():
    """Get discord webhook bot ids.

    :return list: Discord webhook bot ids.
    """
    data = json.load(open('sync_channels.json', 'r', encoding="utf8"))
    discord_channel_webhooks = [entry['discord_channel_webhook'] for entry in data]
    discord_webhook_bot_ids = [int(webhook.split('/')[-2]) for webhook in discord_channel_webhooks]
    return discord_webhook_bot_ids


def download_file_from_url(sub_num, url, filename):
    """Download file from url.

    Use to download any files from discord.

    :param int sub_num: Subscribed sync channels num.
    :param url: url of file
    :param filename: filename of file
    :return str: file path
    """
    r = requests.get(url, allow_redirects=True, timeout=5)
    path = f'./downloads/{sub_num}'
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = f'{path}/{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}_{filename}'
    with open(file_path, 'wb') as fd:
        fd.write(r.content)
    return file_path


def download_file_from_line(sub_num, source, message_type, file_name=None):
    """Get file binary and save them in PC.

    Use to download files from LINE.

    :param int sub_num: Subscribed sync channels num.
    :param source: source of file that given by LINE
    :param message_type: message type from line
    :param file_name: file name of file
    :return str: file path
    """
    file_type = {
        'image': 'jpg',
        'video': 'mp4',
        'audio': 'm4a',
    }
    path = f'./downloads/{sub_num}'
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
