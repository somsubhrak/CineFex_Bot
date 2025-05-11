from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from movieBot import build_bot
import asyncio
from telegram import Update

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

app = Flask(__name__)
telegram_app = build_bot()  # Build the Application instance


async def process_update(update_dict):
    """Processes a single Telegram update."""
    try:
        update = Update.de_json(update_dict, telegram_app.bot)
        await telegram_app.process_update(update)  # Process the update
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error processing update: {e}")


@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    """Handles Telegram updates sent via webhook."""

    if request.headers.get("Content-Type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update_dict = request.get_json()
        asyncio.run(process_update(update_dict))  # Run the async function
        return jsonify({"status": "OK"}), 200
    else:
        return "Invalid Content-Type", 403


@app.route("/")
def index():
    return "Telegram Movie Bot is live via webhook!"


async def set_webhook():
    """Sets the Telegram bot's webhook and initializes the Application."""

    if BASE_URL:
        full_url = f"{BASE_URL}{WEBHOOK_PATH}"
        try:
            webhook_status = await telegram_app.bot.set_webhook(url=full_url)
            if webhook_status:
                print(f"Webhook set to: {full_url}")
            else:
                print(f"Failed to set webhook to: {full_url}")
            await telegram_app.initialize()  # Initialize the Application here
        except Exception as e:
            print(f"Error setting webhook or initializing app: {e}")
    else:
        print("BASE_URL is not set. Webhook not set.")


if __name__ == "__main__":
    asyncio.run(set_webhook())
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)