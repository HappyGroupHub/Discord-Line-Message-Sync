"""This python file will handle line webhooks."""

import json
# from threading import Thread
#
# import zmq
from discord import SyncWebhook
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage

import utilities as utils

config = utils.read_config()
line_bot_api = LineBotApi(config.get('line_channel_access_token'))
handler = WebhookHandler(config.get('line_channel_secret'))
discord_webhook = SyncWebhook.from_url(config.get('discord_channel_webhook'))

app = Flask(__name__)
log = create_logger(app)


# context = zmq.Context()
# socket = context.socket(zmq.SUB)
# socket.connect("tcp://localhost:5555")
# socket.setsockopt_string(zmq.SUBSCRIBE, '')


@app.route("/callback", methods=['POST'])
def callback():
    """Callback function for line webhook."""

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    log.info("Request body: %s", body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """Handle message event."""
    print(debug_json())
    author = line_bot_api.get_profile(event.source.user_id).display_name
    message = event.message.text
    if config.get('line_chat_type') == 'group':
        if event.source.group_id == config.get('line_group_id'):
            discord_webhook.send(f"{author}: {message}", username="Line 訊息")
    if config.get('line_chat_type') == 'user':
        if event.source.user_id == config.get('line_user_id'):
            discord_webhook.send(f"{author}: {message}", username="Line 訊息")


# TODO(LD): zmq
# def receive_from_discord():
#     """Receive message from discord bot."""
#     while True:
#         received = socket.recv_json()
#         received = json.loads(received)
#         line_bot_api.push_message(config.get('line_group_id'),
#                                   TextMessage(
#                                       text=f"{received.get('author')}: {received.get('message')}"))
#
#
# thread = Thread(target=receive_from_discord)
# thread.start()


def debug_json():
    """Debug json.

    :rtype json
    """
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    return json_data


if __name__ == "__main__":
    app.run()
