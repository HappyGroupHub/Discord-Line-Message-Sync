"""This python file will handle line webhooks."""
import json

from discord import SyncWebhook, File
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage, VideoMessage

import utilities as utils

# from threading import Thread
#
# import zmq

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
    if event.message.text == '!ID':
        if event.source.type == 'user':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.source.user_id))
        if event.source.type == 'group':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.source.group_id))
    if config.get('line_chat_type') == 'user':
        if event.source.user_id == config.get('line_user_id'):
            author = line_bot_api.get_profile(event.source.user_id).display_name
            author_image = line_bot_api.get_profile(event.source.user_id).picture_url
            message = event.message.text
            discord_webhook.send(message, username=f"{author} - (Line訊息)", avatar_url=author_image)
    if config.get('line_chat_type') == 'group':
        if event.source.group_id == config.get('line_group_id'):
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            message = event.message.text
            discord_webhook.send(message, username=f"{author} - (Line訊息)", avatar_url=author_image)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    """Handle image message event."""
    if config.get('line_chat_type') == 'user':
        if event.source.user_id == config.get('line_user_id'):
            author = line_bot_api.get_profile(event.source.user_id).display_name
            author_image = line_bot_api.get_profile(event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(source, event.message.type)
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)
    if config.get('line_chat_type') == 'group':
        if event.source.group_id == config.get('line_group_id'):
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(source, event.message.type)
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
    """Handle video message event."""
    if config.get('line_chat_type') == 'user':
        if event.source.user_id == config.get('line_user_id'):
            author = line_bot_api.get_profile(event.source.user_id).display_name
            author_image = line_bot_api.get_profile(event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(source, event.message.type)
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)
    if config.get('line_chat_type') == 'group':
        if event.source.group_id == config.get('line_group_id'):
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(source, event.message.type)
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


# @handler.add(MessageEvent, message=AudioMessage)
# def handle_audio(event):
#     """Handle audio message event."""
#     print(debug_json())
#     if config.get('line_chat_type') == 'user':
#         if event.source.user_id == config.get('line_user_id'):
#             author = line_bot_api.get_profile(event.source.user_id).display_name
#             author_image = line_bot_api.get_profile(event.source.user_id).picture_url
#             file_path = get_file_path(event.message.type, event.message.id)
#             discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
#                                  avatar_url=author_image)
#     if config.get('line_chat_type') == 'group':
#         if event.source.group_id == config.get('line_group_id'):
#             print(debug_json())
#             author = line_bot_api.get_group_member_profile(event.source.group_id,
#                                                            event.source.user_id).display_name
#             author_image = line_bot_api.get_group_member_profile(event.source.group_id,
#                                                                  event.source.user_id).picture_url
#             message = event.message.text
#             discord_webhook.send(message, username=f"{author} - (Line訊息)", avatar_url=author_image)
#
#
# @handler.add(MessageEvent, message=FileMessage)
# def handle_file(event):
#     """Handle file message event."""
#     print(debug_json())
#     if config.get('line_chat_type') == 'user':
#         if event.source.user_id == config.get('line_user_id'):
#             author = line_bot_api.get_profile(event.source.user_id).display_name
#             author_image = line_bot_api.get_profile(event.source.user_id).picture_url
#             file_path = get_file_path(event.message.type, event.message.id)
#             discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
#                                  avatar_url=author_image)
#     if config.get('line_chat_type') == 'group':
#         if event.source.group_id == config.get('line_group_id'):
#             print(debug_json())
#             author = line_bot_api.get_group_member_profile(event.source.group_id,
#                                                            event.source.user_id).display_name
#             author_image = line_bot_api.get_group_member_profile(event.source.group_id,
#                                                                  event.source.user_id).picture_url
#             message = event.message.text
#             discord_webhook.send(message, username=f"{author} - (Line訊息)", avatar_url=author_image)
#
#
# @handler.add(MessageEvent, message=StickerMessage)
# def handle_sticker(event):
#     """Handle sticker message event."""
#     print(debug_json())
#     if config.get('line_chat_type') == 'user':
#         if event.source.user_id == config.get('line_user_id'):
#             author = line_bot_api.get_profile(event.source.user_id).display_name
#             author_image = line_bot_api.get_profile(event.source.user_id).picture_url
#             file_path = get_file_path(event.message.type, event.message.id)
#             discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
#                                  avatar_url=author_image)
#     if config.get('line_chat_type') == 'group':
#         if event.source.group_id == config.get('line_group_id'):
#             print(debug_json())
#             author = line_bot_api.get_group_member_profile(event.source.group_id,
#                                                            event.source.user_id).display_name
#             author_image = line_bot_api.get_group_member_profile(event.source.group_id,
#                                                                  event.source.user_id).picture_url
#             message = event.message.text
#             discord_webhook.send(message, username=f"{author} - (Line訊息)", avatar_url=author_image)


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
