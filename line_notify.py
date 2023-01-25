"""This python file will send messages to LINE Notify."""

import requests

import utilities as utils

config = utils.read_config()


def send_message(sub_num, message):
    """Send message to LINE Notify.

    :param int sub_num: Subscribed sync channels num.
    :param str message: Message to send.
    """
    token = config.get(f'line_notify_token_{sub_num}')
    headers = {"Authorization": "Bearer " + token}
    data = {'message': message}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, timeout=5)


def send_image_message(sub_num, message, image_path):
    """Send media message to LINE Notify.

    :param int sub_num: Subscribed sync channels num.
    :param str message: Message to send.
    :param str image_path: Path to media.
    """
    token = config.get(f'line_notify_token_{sub_num}')
    headers = {"Authorization": "Bearer " + token}
    data = {'message': message}
    with open(image_path, 'rb') as f:
        image = f.read()
    files = {'imageFile': image}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, files=files, timeout=5)
