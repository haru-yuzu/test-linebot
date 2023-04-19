from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)
app.debug = False
# Herokuの環境変数に設定されたLINEDevelopersのアクセストークン、チャンネルシークレット取得
MY_CHANNEL_ACCESS_TOKEN = os.environ["Ob8Pm3gabHuODgTZ3xelp4HT5LjFzgJ2/91y6QV3mJ0ho74ZN12JXpczXTEjdtC+OpqE3LrS980\
                                        hwrQLlofl+qUzEuS9GvIDIc8Xl/YJy9o6RoWkYJ4t1gK+aGYsACa+t34CyX6gKsNDM+hwSWd22\
                                        AdB04t89/1O/w1cDnyilFU="]
MY_CHANNEL_SECRET = os.environ["d21d5db1cf86fa1cc847f444a8833e2e"]
line_bot_api = LineBotApi(MY_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(MY_CHANNEL_SECRET)


# Herokuにデプロイが成功したときに表示する
@app.route("/")
def hello_world():
    return "hello world!"


# LINE DevelopersのWebhookにURLを指定してイベントが送られるようにする
@app.route("/callback", methods='POST')
def callback():
    # リクエストヘッダーから署名検証のための値取得
    signature = request.headers['X-Line-Signature']
    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("request body: " + body)

    # 署名の検証、handleに定義されている関数の呼び出し
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check youe channel access token/channel secret.")
        abort(400)
    return 'OK'


# webhookから送られてきたイベントの処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


# ポート番号
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
