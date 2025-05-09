from flask import Flask
import os
from dotenv import load_dotenv
from movieBot import run_bot 

load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return "Movie recommendation bot is running."

if __name__ == '__main__':
    run_bot()  
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
