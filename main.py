from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv
from movieBot import run_bot  # Don't override this

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return "Movie recommendation bot is running."

if __name__ == '__main__':
    Thread(target=run_bot).start()  # Correctly call the actual function
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
