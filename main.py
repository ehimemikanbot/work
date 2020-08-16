from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FlexSendMessage,BubbleContainer
)
import os
import json

app = Flask(__name__)


# 環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
 
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)
 
menu = {
  "type": "template",
  "altText": "this is a buttons template",
  "template": {
    "type": "buttons",
    "actions": [
      {
        "type": "message",
        "label": "引越し",
        "text": "引越し"
      },
      {
        "type": "message",
        "label": "アクション 2",
        "text": "アクション 2"
      },
      {
        "type": "message",
        "label": "アクション 3",
        "text": "アクション 3"
      },
      {
        "type": "message",
        "label": "アクション 4",
        "text": "アクション 4"
      }
    ],
    "title": "質問メニュー",
    "text": "聞きたい内容を以下から選んでください"
  }
}

## 1 ##
# Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証のための値を取得
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている〜〜
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@app.route("/index", methods=['POST'])
def index():
    return 'OK'

## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
 
#LINEでMessageEvent（普通のメッセージを送信された場合）が起こった場合に、
#def以下の関数を実行します。
#reply_messageの第一引数のevent.reply_tokenは、イベントの応答に用いるトークンです。 
#第二引数には、linebot.modelsに定義されている返信用のTextSendMessageオブジェクトを渡しています。
 
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    #FlexMessage
    container_obj = BubbleContainer.new_from_json_dict(menu)

    #line_bot_api.reply_message(
    #    event.reply_token,
    #    TextSendMessage(text=event.message.text)) #ここでオウム返しのメッセージを返します。
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(alt_text="items",contents=BubbleContainer.new_from_json_dict(json.load(menu)))
    )
 
# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
