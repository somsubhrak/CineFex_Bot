from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
    CommandHandler,
)
from telegram.helpers import escape_markdown
import requests
import os
from dotenv import load_dotenv
from genreMap import GENRE_MAP
import random

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Validate API key and bot token
if not BOT_TOKEN or not TMDB_API_KEY:
    raise ValueError("BOT_TOKEN or TMDB_API_KEY is not set. Please check your .env file.")


# Format movie
def format_movies(results: list) -> list[tuple[str, str | None]]:
    recommendations = []
    for movie in results:
        title = movie.get("title", "Untitled")
        year = movie.get("release_date", "N/A")[:4] if movie.get("release_date") else "N/A"
        overview = movie.get("overview", "No description available.")
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        title = escape_markdown(title, version=2)
        year = escape_markdown(year, version=2)
        overview = escape_markdown(overview, version=2)

        text = f"*{title}* ({year})\n_{overview}_"  # Adjusted escaping
        recommendations.append((text, poster_url))
    return recommendations


def extract_genre_ids(prompt: str) -> str:
    prompt = prompt.lower()
    genre_ids = [str(genre_id) for keyword, genre_id in GENRE_MAP.items() if keyword in prompt]
    return ",".join(genre_ids)


def get_recommendations(prompt: str) -> list[tuple[str, str | None]]:
    genre_id = extract_genre_ids(prompt)
    try:
        if genre_id:
            url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}"
        else:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={prompt}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])[:5]
        return format_movies(results)
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []


def get_random_movie() -> list[tuple[str, str | None]]:
    try:
        page = random.randint(1, 500)
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=popularity.desc&page={page}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            return format_movies([random.choice(results)])
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []


async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input:
        await update.message.reply_text("Please type something to get a movie recommendation.")
        return
    recs = get_recommendations(user_input)
    await send_recommendations(update, recs)


async def send_recommendations(update: Update, recs: list[tuple[str, str | None]]):
    if not recs:
        await update.message.reply_text("No recommendations found. Try again later.")
        return
    for text, poster_url in recs:
        try:
            if poster_url:
                await update.message.reply_photo(
                    photo=poster_url, caption=text, parse_mode="MarkdownV2"
                )
            else:
                await update.message.reply_text(text, parse_mode="MarkdownV2")
        except Exception:
            await update.message.reply_text(
                "Sorry, there was an error displaying the movie.", parse_mode="MarkdownV2"
            )


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Send me a movie name or genre, and I'll recommend something!\nTry /random for a surprise movie!"
    )


async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recs = get_random_movie()
    await send_recommendations(update, recs)


def build_bot() -> Application:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("random", random_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))
    return app