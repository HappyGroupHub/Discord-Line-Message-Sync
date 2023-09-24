"""This python file will send messages to LINE Notify."""
import urllib

import requests

import utilities as utils

config = utils.read_config()
webhook_url = config['webhook_url']
line_notify_id = config['line_notify_id']
line_notify_secret = config['line_notify_secret']


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


def create_auth_link(state):
    """Create LINE Notify auth link for user to connect.

    :param str state: The state to pass to LINE Notify.
    :return str: The auth link.
    """
    data = {
        'response_type': 'code',
        'client_id': line_notify_id,
        'redirect_uri': webhook_url + '/notify',
        'scope': 'notify',
        'state': state,
        'response_mode': 'form_post'
    }
    query_str = urllib.parse.urlencode(data)
    return f'https://notify-bot.line.me/oauth/authorize?{query_str}'


def get_notify_token_by_auth_code(auth_code):
    """Get LINE Notify token by auth code.

    :param str auth_code: The auth code.
    :return str: Line notify token of the user.
    """
    url = 'https://notify-bot.line.me/oauth/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': webhook_url + '/notify',
        'client_id': line_notify_id,
        'client_secret': line_notify_secret
    }
    response = requests.post(url, data=data, headers=headers)
    notify_token = response.json()['access_token']
    return notify_token
