import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message

#from libretranslatepy import LibreTranslateAP

load_dotenv()


machine = TocMachine(
    states=["user", "start", "language", "chinese", "german", "french", "prison",
    "prison", "nobody", "friend", "date", "software", "chat", "home", "bff", 
    "think", "go", "harass", "poem"],
    transitions=[
        {
            "trigger": "advance",
            "source": "user",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "software",
            "conditions": "is_going_to_software",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "language",
            "conditions": "is_going_to_language",
        },
        {
            "trigger": "advance",
            "source": "language",
            "dest": "chinese",
            "conditions": "is_going_to_chinese",
        },
        {
            "trigger": "advance",
            "source": "language",
            "dest": "german",
            "conditions": "is_going_to_german",
        },
        {
            "trigger": "advance",
            "source": "language",
            "dest": "french",
            "conditions": "is_going_to_french",
        },
        {
            "trigger": "advance",
            "source": "chinese",
            "dest": "prison",
            "conditions": "is_going_to_prison",
        },
        {
            "trigger": "advance",
            "source": "chinese",
            "dest": "nobody",
            "conditions": "is_going_to_nobody",
        },
        {
            "trigger": "advance",
            "source": "chinese",
            "dest": "friend",
            "conditions": "is_going_to_friend",
        },
        {
            "trigger": "advance",
            "source": "friend",
            "dest": "chat",
            "conditions": "is_going_to_chat",
        },
        {
            "trigger": "advance",
            "source": "friend",
            "dest": "home",
            "conditions": "is_going_to_home",
        },
        {
            "trigger": "advance",
            "source": "chat",
            "dest": "date",
            "conditions": "is_going_to_date",
        },
        {
            "trigger": "advance",
            "source": "chat",
            "dest": "bff",
            "conditions": "is_going_to_bff",
        },
        {
            "trigger": "advance",
            "source": "date",
            "dest": "think",
            "conditions": "is_going_to_think",
        },
        {
            "trigger": "advance",
            "source": "date",
            "dest": "go",
            "conditions": "is_going_to_go",
        },
        {
            "trigger": "advance",
            "source": "german",
            "dest": "harass",
            "conditions": "is_going_to_harass",
        },
        {
            "trigger": "advance",
            "source": "german",
            "dest": "poem",
            "conditions": "is_going_to_poem",
        },
        {
            "trigger": "advance",
            "source": "poem",
            "dest": "nobody",
            "conditions": "is_going_to_nobody",
        },
        {
            "trigger": "advance",
            "source": "poem",
            "dest": "bff",
            "conditions": "is_going_to_bff",
        },
        {"trigger": "go_back", "source": ["prison", "nobody", "date", "software", "home", "bff", "go", "think", "harass", "poem", "french"],
        "dest": "user"},
    ],
    initial="user",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        mstate=machine.state
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            send_text_message(event.reply_token, mstate)
            #send_text_message(event.reply_token, mstate)

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="127.0.0.1", port=port, debug=True)
