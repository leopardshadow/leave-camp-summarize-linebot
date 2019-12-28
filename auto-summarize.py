from flask import Flask, request, abort
import re

import config as cfg

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

line_bot_api = LineBotApi(cfg.channel_access_token)
handler = WebhookHandler(cfg.channel_secret)


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
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    in_msg = event.message.text


    if in_msg == ':clear_all':

        init_msgs()

    status, num, msg = process_in_msg(in_msg)

    if status == False:
        return

    global msgs
    # msgs.append(in_msg)
    msgs[num] = msg

    
    # if text == '/help':
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text='~~HELP~~'))

    # if text == '/list':
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(text='~~LIST~~'))

    # purly echo 
    # else:

    ret_msg = ''
    for num, msg in msgs.items():
        ret_msg = ret_msg + '{:03d} {}\n'.format(num, msg) 

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ret_msg))

"""
Format:
-------
報告班長
日期：12/25
號碼：XX
時間：12:00
地點：[哪]
跟誰：[誰]
做什麼：[什麼事]

XX在[哪]跟[誰]做[什麼事]
跟[誰]: 自己就不顯示

"""

def process_in_msg(in_msg):

    try:
        num = re.findall("號碼[:：](.*)", in_msg)[0]
        loc = '在' + re.findall("地點[:：](.*)", in_msg)[0]
        who = '跟' + re.findall("跟誰[:：](.*)", in_msg)[0]
        if who == '跟自己':
            who = ''
        what = re.findall("做什麼[:：](.*)", in_msg)[0]

        msg = ' {} {} {}'.format(loc, who, what)
        print(msg)

        return True, int(num), msg

    except Exception as e:
        return False, 0, ""


def init_msgs():

    global msgs
    msgs = dict([(44, ''),
                 (45, ''),
                 (46, ''),
                 (47, ''),
                 (48, ''),
                 (49, ''),
                 (50, ''),
                 (51, ''),
                 (52, ''),
                 (53, ''),
                 (54, ''),
                 (55, ''),
                 (56, ''),
                 (57, ''),
                ])



if __name__ == "__main__":

    global msgs
    init_msgs()

    app.run(port=1234, debug=True)

