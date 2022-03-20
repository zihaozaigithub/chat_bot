from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('kb2CG1Pp40qk5QYWXdjtSz2Mqlc3CVyaDtKtz+B08mQtjOXTt5O+eDSox8bXS+kAhGiuj1CgPw2kUfVR8gcdblqBuF//C2Tq90Z3h6iEzwCortSO7ZtmGr8b9w3LT8lacoVlXf66EIVcfB/Gph9oOwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('23f990e781530b767e597ca88a529713')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()