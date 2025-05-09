from flask import Flask, request
import os
from dotenv import load_dotenv
from movieBot import build_bot

load_dotenv()

app = Flask(__name__)
telegram_app = build_bot()

# Get from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("BASE_URL")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

@app.route('/')
def index():
    return "Telegram Movie Bot (Webhook version) is running."

@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    await telegram_app.update_queue.put(await telegram_app.request.parse_update(request.get_data()))
    return '', 200

@app.before_first_request
def setup_webhook():
    if BASE_URL:
        url = f"{BASE_URL}{WEBHOOK_PATH}"
        telegram_app.bot.set_webhook(url=url)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
