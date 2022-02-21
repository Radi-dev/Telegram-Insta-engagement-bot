from flask import Flask, request
from config import os, TOKEN, DEBUG
from waitress import serve
from main.teleg_bot import updater


app = Flask(__name__)


@app.route('/' + TOKEN, methods=['POST', 'GET'])
def getMessage():
    return "running", 200


@app.route("/")
def reset_webhook():
    return "Running", 200


if __name__ == "__main__":
    if DEBUG:

        updater.start_polling()
        # for i in range(1000000):
        #    print(i**i)
        # app.run(debug=True, host="0.0.0.0",
        #       port=int(os.environ.get('PORT', 80)))
    else:
        serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
