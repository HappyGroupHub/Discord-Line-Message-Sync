"""This python file will send messages to LINE Notify."""

import requests

import utilities as utils

config = utils.read_config()


def send_message(message, notify_token):
    """Send message to LINE Notify.

    :param str message: Message to send.
    :param str notify_token: LINE Notify token.
    """
    headers = {"Authorization": "Bearer " + notify_token}
    data = {'message': message}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, timeout=5)


def send_image_message(message, image_path, notify_token):
    """Send media message to LINE Notify.

    :param str message: Message to send.
    :param str image_path: Path to media.
    :param str notify_token: LINE Notify token.
    """
    headers = {"Authorization": "Bearer " + notify_token}
    data = {'message': message}
    with open(image_path, 'rb') as f:
        image = f.read()
    files = {'imageFile': image}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, files=files, timeout=5)
