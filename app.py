from flask import Flask, request
from config import os, TOKEN, DEBUG, WEBHOOK_URL
from waitress import serve
from main.teleg_bot import updater, Bot


app = Flask(__name__)


@app.route('/' + TOKEN, methods=['POST', 'GET'])
def getMessage():
    return "running", 200


@app.route("/")
def reset_webhook():
    # Bot.delete_webhook()
    Bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "Running", 200


if __name__ == "__main__":
    if DEBUG:
        # Bot.delete_webhook()
        updater.start_polling()

    else:
        updater.start_webhook(listen="127.0.0.1",
                              port=80,
                              webhook_url=WEBHOOK_URL,
                              url_path=TOKEN)
        #updater.bot.setWebhook("YOUR WEB SERVER LINK HERE" + "YOUR TOKEN HERE")
        updater.idle()
        # for dev
        #app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))
        # for production
        # #serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
