"""This python file will send messages to LINE Notify."""

import requests

import utilities as utils

config = utils.read_config()


def send_message(message):
    """Send message to LINE Notify."""

    token = config.get('line_notify_token')
    headers = {"Authorization": "Bearer " + token}
    data = {'message': message}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data)


def send_image_message(message, image_path):
    """Send image message to LINE Notify."""

    token = config.get('line_notify_token')
    headers = {"Authorization": "Bearer " + token}
    data = {'message': message}
    image = open(image_path, 'rb')
    files = {'imageFile': image}
    requests.post("https://notify-api.line.me/api/notify",
                  headers=headers, data=data, files=files)
