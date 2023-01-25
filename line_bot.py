"""This python file will handle line webhooks."""
import json

from discord import SyncWebhook, File
from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage, VideoMessage

import utilities as utils

config = utils.read_config()
line_bot_api = LineBotApi(config.get('line_channel_access_token'))
handler = WebhookHandler(config.get('line_channel_secret'))

app = Flask(__name__)
log = create_logger(app)


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


def debug_json():
    """Debug json.

    :rtype json
    """
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    return json_data


if __name__ == "__main__":
    app.run()
