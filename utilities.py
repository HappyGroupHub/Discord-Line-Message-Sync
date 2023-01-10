"""This python file will handle some extra functions."""

import sys

import yaml
from yaml import SafeLoader


def read_config():
    """Read config file.

    Check if config file exists, if not, create one.
    if exists, read config file and return config with dict type.

    :rtype: dict
    """
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
    except FileNotFoundError:
        print("Config file not found, create one by default.\nPlease finish filling config.yml")
        with open('config.yml', 'w', encoding="utf8") as f:
            f.write(
                "Line:\n  channel_access_token: ''\n  channel_secret: ''\n  line_notify_token: ''\n"
                "\n  # 以下為聊天室綁定設定:\n  # 聊天室屬性, 目前只有私人訊息以及群組訊息兩種 (user, group)\n"
                "  chat_type: ''\n\n  # 私人訊息: 請在user_id填入你的line_user_id\n"
                "  # 群組訊息: 請在group_id填入你的群組id\n  # 依照上面聊天室屬性對應填入一個即可\n"
                "  user_id: ''\n  group_id: ''\n\n"
                "Discord:\n  bot_token: ''\n channel_id: ''\n  channel_webhook: ''\n")
        sys.exit()
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
    return webhook_url.split('/')[-2]
