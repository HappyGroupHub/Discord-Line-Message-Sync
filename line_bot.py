"""This python file will handle line webhooks."""

from flask import Flask, request, abort
from flask.logging import create_logger
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError

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


if __name__ == "__main__":
    app.run()
