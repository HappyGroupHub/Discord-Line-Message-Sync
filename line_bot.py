"""This python file will handle line webhooks."""
import json
from threading import Thread

import zmq
from discord import SyncWebhook, File
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, VideoMessage, VideoSendMessage, \
    TextSendMessage, AudioMessage, AudioSendMessage

import line_notify
import utilities as utils

config = utils.read_config()
line_bot_api = LineBotApi(config.get('line_channel_access_token'))
handler = WebhookHandler(config.get('line_channel_secret'))

app = Flask(__name__)
log = create_logger(app)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, '')


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
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        if event.message.text == '!ID':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=event.source.group_id))
        if event.source.group_id in config.get('subscribed_line_channels'):
            sub_num = config.get('subscribed_line_channels').index(event.source.group_id) + 1
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            message = event.message.text
            discord_webhook = SyncWebhook.from_url(config.get(f'discord_channel_webhook_{sub_num}'))
            discord_webhook.send(message, username=f"{author} - (Line訊息)", avatar_url=author_image)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    """Handle image message event."""
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        if event.source.group_id in config.get('subscribed_line_channels'):
            sub_num = config.get('subscribed_line_channels').index(event.source.group_id) + 1
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(sub_num, source, event.message.type)
            discord_webhook = SyncWebhook.from_url(config.get(f'discord_channel_webhook_{sub_num}'))
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
    """Handle video message event."""
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        if event.source.group_id in config.get('subscribed_line_channels'):
            sub_num = config.get('subscribed_line_channels').index(event.source.group_id) + 1
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(sub_num, source, event.message.type)
            discord_webhook = SyncWebhook.from_url(config.get(f'discord_channel_webhook_{sub_num}'))
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    """Handle audio message event."""
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        if event.source.group_id in config.get('subscribed_line_channels'):
            sub_num = config.get('subscribed_line_channels').index(event.source.group_id) + 1
            author = line_bot_api.get_group_member_profile(event.source.group_id,
                                                           event.source.user_id).display_name
            author_image = line_bot_api.get_group_member_profile(event.source.group_id,
                                                                 event.source.user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(sub_num, source, event.message.type)
            discord_webhook = SyncWebhook.from_url(config.get(f'discord_channel_webhook_{sub_num}'))
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


def debug_json():
    """Debug json.

    :rtype json
    """
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    return json_data


def receive_from_discord():
    """Receive from discord bot."""
    while True:
        received = socket.recv_json()
        received = json.loads(received)
        if received.get('msg_type') == 'video':
            group_id = config.get(f"line_group_id_{received.get('sub_num')}")
            message = received.get('message')
            if message == "":
                message = f"{received.get('author')}: 傳送了影片"
            else:
                message = f"{received.get('author')}: {message}(影片)"
            line_notify.send_message(received.get('sub_num'), message)
            line_bot_api.push_message(group_id,
                                      VideoSendMessage(
                                          original_content_url=received.get('video_url'),
                                          preview_image_url=received.get('thumbnail_url')))
        if received.get('msg_type') == 'audio':
            group_id = config.get(f"line_group_id_{received.get('sub_num')}")
            message = received.get('message')
            if message == "":
                message = f"{received.get('author')}: 傳送了音訊"
            else:
                message = f"{received.get('author')}: {message}(音訊)"
            line_notify.send_message(received.get('sub_num'), message)
            line_bot_api.push_message(group_id,
                                      AudioSendMessage(
                                          original_content_url=received.get('audio_url'),
                                          duration=received.get('audio_duration')))


thread = Thread(target=receive_from_discord)
thread.start()

if __name__ == "__main__":
    app.run()
