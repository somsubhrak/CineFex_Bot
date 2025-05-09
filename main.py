from flask import Flask, request
import os
from dotenv import load_dotenv
from movieBot import build_bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # e.g., https://your-render-app.onrender.com
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

app = Flask(__name__)
telegram_app = build_bot()  # Assuming this returns a telegram.ext.Application instance

# Webhook route
@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = await telegram_app.request.parse_update(await request.get_data())
    await telegram_app.update_queue.put(update)
    return '', 200

@app.route('/')
def index():
    return "Telegram Movie Bot is live via webhook!"

def set_webhook():
    if BASE_URL:
        full_url = f"{BASE_URL}{WEBHOOK_PATH}"
        print(f"Setting webhook to: {full_url}")
        telegram_app.bot.set_webhook(url=full_url)

if __name__ == '__main__':
    # Set webhook BEFORE starting the app
    set_webhook()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request
import os
from dotenv import load_dotenv
from movieBot import build_bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # e.g., https://your-render-app.onrender.com
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

app = Flask(__name__)
telegram_app = build_bot()  # Assuming this returns a telegram.ext.Application instance

# Webhook route
@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = await telegram_app.request.parse_update(await request.get_data())
    await telegram_app.update_queue.put(update)
    return '', 200

@app.route('/')
def index():
    return "Telegram Movie Bot is live via webhook!"

def set_webhook():
    if BASE_URL:
        full_url = f"{BASE_URL}{WEBHOOK_PATH}"
        print(f"Setting webhook to: {full_url}")
        telegram_app.bot.set_webhook(url=full_url)

if __name__ == '__main__':
    # Set webhook BEFORE starting the app
    set_webhook()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request
import os
from dotenv import load_dotenv
from movieBot import build_bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")  # e.g., https://your-render-app.onrender.com
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

app = Flask(__name__)
telegram_app = build_bot()  # Assuming this returns a telegram.ext.Application instance

# Webhook route
@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = await telegram_app.request.parse_update(await request.get_data())
    await telegram_app.update_queue.put(update)
    return '', 200

@app.route('/')
def index():
    return "Telegram Movie Bot is live via webhook!"

def set_webhook():
    if BASE_URL:
        full_url = f"{BASE_URL}{WEBHOOK_PATH}"
        print(f"Setting webhook to: {full_url}")
        telegram_app.bot.set_webhook(url=full_url)

if __name__ == '__main__':
    # Set webhook BEFORE starting the app
    set_webhook()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request
import os
from dotenv import load_dotenv
from movieBot import build_bot

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL") 
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

app = Flask(__name__)
telegram_app = build_bot()  


@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = await telegram_app.request.parse_update(await request.get_data())
    await telegram_app.update_queue.put(update)
    return '', 200

@app.route('/')
def index():
    return "Telegram Movie Bot is live via webhook!"

def set_webhook():
    if BASE_URL:
        full_url = f"{BASE_URL}{WEBHOOK_PATH}"
        print(f"Setting webhook to: {full_url}")
        telegram_app.bot.set_webhook(url=full_url)

if __name__ == '__main__':

    set_webhook()

    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
