"""This python file will handle line webhooks."""
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
    try:
        if event.source.group_id == config.get('line_group_id'):
            author = line_bot_api.get_profile(event.source.user_id).display_name
            message = event.message.text
            discord_webhook.send(f"{author}: {message}", username="LD's Automation Bot")
        else:
            print("Message is not from assigned group.")
    except AttributeError:
        print("This message is not from a group.")
        pass


if __name__ == "__main__":
    app.run()
