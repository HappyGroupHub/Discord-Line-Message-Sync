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
line_bot_api = LineBotApi(config['line_channel_access_token'])
handler = WebhookHandler(config['line_channel_secret'])

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
        message_received = event.message.text
        user_id = event.source.user_id
        group_id = event.source.group_id
        reply_token = event.reply_token
        subscribed_line_channels = utils.get_subscribed_line_channels()
        if message_received == '!ID':
            line_bot_api.reply_message(reply_token, TextSendMessage(text=group_id))
        if group_id in subscribed_line_channels:
            subscribed_info = utils.get_subscribed_info_by_line_group_id(group_id)
            author = line_bot_api.get_group_member_profile(group_id, user_id).display_name
            author_image = line_bot_api.get_group_member_profile(group_id, user_id).picture_url
            discord_webhook = SyncWebhook.from_url(subscribed_info['discord_channel_webhook'])
            discord_webhook.send(message_received, username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    """Handle image message event."""
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        user_id = event.source.user_id
        group_id = event.source.group_id
        subscribed_line_channels = utils.get_subscribed_line_channels()
        if group_id in subscribed_line_channels:
            subscribed_info = utils.get_subscribed_info_by_line_group_id(group_id)
            author = line_bot_api.get_group_member_profile(group_id, user_id).display_name
            author_image = line_bot_api.get_group_member_profile(group_id, user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(subscribed_info['sub_num'], source,
                                                      event.message.type)
            discord_webhook = SyncWebhook.from_url(subscribed_info['discord_channel_webhook'])
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


@handler.add(MessageEvent, message=VideoMessage)
def handle_video(event):
    """Handle video message event."""
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        user_id = event.source.user_id
        group_id = event.source.group_id
        subscribed_line_channels = utils.get_subscribed_line_channels()
        if group_id in subscribed_line_channels:
            subscribed_info = utils.get_subscribed_info_by_line_group_id(group_id)
            author = line_bot_api.get_group_member_profile(group_id, user_id).display_name
            author_image = line_bot_api.get_group_member_profile(group_id, user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(subscribed_info['sub_num'], source,
                                                      event.message.type)
            discord_webhook = SyncWebhook.from_url(subscribed_info['discord_channel_webhook'])
            discord_webhook.send(file=File(file_path), username=f"{author} - (Line訊息)",
                                 avatar_url=author_image)


@handler.add(MessageEvent, message=AudioMessage)
def handle_audio(event):
    """Handle audio message event."""
    if event.source.type == 'user':
        return
    if event.source.type == 'group':
        user_id = event.source.user_id
        group_id = event.source.group_id
        subscribed_line_channels = utils.get_subscribed_line_channels()
        if group_id in subscribed_line_channels:
            subscribed_info = utils.get_subscribed_info_by_line_group_id(group_id)
            author = line_bot_api.get_group_member_profile(group_id, user_id).display_name
            author_image = line_bot_api.get_group_member_profile(group_id, user_id).picture_url
            source = line_bot_api.get_message_content(event.message.id)
            file_path = utils.download_file_from_line(subscribed_info['sub_num'], source,
                                                      event.message.type)
            discord_webhook = SyncWebhook.from_url(subscribed_info['discord_channel_webhook'])
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
        subscribed_info = utils.get_subscribed_info_by_sub_num(received['sub_num'])
        group_id = subscribed_info['line_group_id']
        message = received['message']
        if received['msg_type'] == 'video':
            if message == "":
                message = f"{received['author']}: 傳送了影片"
            else:
                message = f"{received['author']}: {message}(影片)"
            line_notify.send_message(message, subscribed_info['line_notify_token'])
            line_bot_api.push_message(group_id,
                                      VideoSendMessage(
                                          original_content_url=received['video_url'],
                                          preview_image_url=received['thumbnail_url']))
        if received['msg_type'] == 'audio':
            if message == "":
                message = f"{received['author']}: 傳送了音訊"
            else:
                message = f"{received['author']}: {message}(音訊)"
            line_notify.send_message(message, subscribed_info['line_notify_token'])
            line_bot_api.push_message(group_id,
                                      AudioSendMessage(
                                          original_content_url=received['audio_url'],
                                          duration=received['audio_duration']))


thread = Thread(target=receive_from_discord)
thread.start()

if __name__ == "__main__":
    app.run()
