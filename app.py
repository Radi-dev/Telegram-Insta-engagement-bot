from flask import Flask, request
from config import os, TOKEN, DEBUG, WEBHOOK_URL
from waitress import serve
from main.teleg_bot import updater, bot, Update
from main.teleg_bot_wbhk import dispatcher, setup_for_Flask
from handlers.deleter import delete


app = Flask(__name__)


@app.route('/' + TOKEN, methods=['POST', 'GET'])
def getMessage():
    update = Update.de_json(
        request.get_json(force=True), bot)
    dispatcher.process_update(update)
    delete()
    return "running", 200


@app.route("/")
def reset_webhook():
    updater.bot.delete_webhook()
    updater.bot.set_webhook(url=WEBHOOK_URL + TOKEN)
    return "Running", 200


# All false to use flask builting
# Set use_polling true for polling
use_polling = True
# Set only use_builtin_server true for python telegram bot's builtin test server
use_builtin_server = False
# Set only use_waitress_server true for production server
use_waitress_server = False
if __name__ == "__main__":

    if use_polling:
        # updater.bot.delete_webhook()
        updater.bot.delete_webhook()
        updater.start_polling()
        print("*****************Start polling..*****************")

    elif use_builtin_server:
        updater.bot.delete_webhook()
        updater.start_webhook(listen="0.0.0.0",
                              port=80,
                              webhook_url=WEBHOOK_URL + TOKEN,
                              )

        print("*****************Using Pyteleg builtin server*****************")
        updater.idle()
    elif not use_waitress_server:
        # for dev
        setup_for_Flask()
        print("*****************Using Flask builtin server*****************")
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=WEBHOOK_URL + TOKEN)
        app.run(debug=DEBUG, host="0.0.0.0",
                port=int(os.environ.get('PORT', 80)), threaded=True)
    else:
        # for production
        setup_for_Flask()
        print("*****************Using Waitress production server*****************")
        updater.bot.delete_webhook()
        updater.bot.set_webhook(url=WEBHOOK_URL + TOKEN)
        serve(app, host='0.0.0.0', port=int(
            os.environ.get('PORT', 80)))
