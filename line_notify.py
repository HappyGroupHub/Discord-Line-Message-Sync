"""This python file will send messages to LINE Notify."""

import requests

import utilities as utils

config = utils.read_config()


def send_message(message):
    """Send message to LINE Notify.

    :param str message: Message to send.
    """
    token = config.get('line_notify_token')
    headers = {"Authorization": "Bearer " + token}
    data = {'message': message}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, timeout=5)


def send_image_message(message, image_path):
    """Send media message to LINE Notify.

    :param str message: Message to send.
    :param str image_path: Path to media.
    """
    token = config.get('line_notify_token')
    headers = {"Authorization": "Bearer " + token}
    data = {'message': message}
    with open(image_path, 'rb') as image:
        files = {'imageFile': image}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, files=files, timeout=5)
