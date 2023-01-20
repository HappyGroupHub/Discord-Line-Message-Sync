"""This python file will handle some extra functions."""
import datetime
import sys
from os.path import exists

import requests
import yaml
from yaml import SafeLoader


def config_file_generator():
    """Generate the template of config file"""
    with open('config.yml', 'w', encoding="utf8") as f:
        f.write("""Line:
  channel_access_token: ''
  channel_secret: ''
  line_notify_token: ''

  # 以下為聊天室綁定設定:
  # 聊天室屬性, 目前只有私人訊息以及群組訊息兩種 (user, group)
  chat_type: ''

  # 私人訊息: 請在user_id填入你的line_user_id
  # 群組訊息: 請在group_id填入你的群組id
  # 依照上面聊天室屬性對應填入一個即可
  user_id: ''
  group_id: ''

Discord:
  bot_token: ''
  channel_id: ''
  channel_webhook: ''
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
        with open('config.yml', 'w', encoding="utf8") as f:
            config_file_generator()

    try:
        with open('config.yml', 'r', encoding="utf8") as f:
            data = yaml.load(f, Loader=SafeLoader)
            config = {
                'line_channel_secret': data['Line']['channel_secret'],
                'line_channel_access_token': data['Line']['channel_access_token'],
                'line_notify_token': data['Line']['line_notify_token'],
                'line_chat_type': data['Line']['chat_type'],
                'line_user_id': data['Line']['user_id'],
                'line_group_id': data['Line']['group_id'],
                'discord_bot_token': data['Discord']['bot_token'],
                'discord_channel_id': data['Discord']['channel_id'],
                'discord_channel_webhook': data['Discord']['channel_webhook']
            }
            return config
    except (KeyError, TypeError):
        print(
            "An error occurred while reading config.yml, please check if the file is corrected filled.\n"
            "If the problem can't be solved, consider delete config.yml and restart the program.\n")
        sys.exit()


def get_discord_webhook_id():
    """Get discord webhook id.

    :rtype: int
    """
    webhook_url = read_config().get('discord_channel_webhook')
    return int(webhook_url.split('/')[-2])


def download_file_from_url(url, filename):
    """Download file from url.

    Use to download any files from discord.

    :param url: url of file
    :param filename: filename of file
    :return str: file path
    """
    file_path = './' + datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '_' + filename
    r = requests.get(url, allow_redirects=True)
    open(file_path, 'wb').write(r.content)
    return file_path


def download_file_from_line(source, message_type, file_name=None):
    """Get file binary and save them in PC.

    Use to download files from LINE.

    :param source: source of file that given by LINE
    :param message_type: message type from line
    :param file_name: file name of file
    :return str: file path
    """
    file_type = {
        'image': 'jpg',
        'video': 'mp4',
    }
    file_path = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + '.' + file_type.get(
        message_type)
    with open(file_path, 'wb') as fd:
        for chunk in source.iter_content():
            fd.write(chunk)
    return file_path
