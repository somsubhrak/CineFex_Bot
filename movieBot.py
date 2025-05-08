from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
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
def format_movies(results):
    recommendations = []
    for movie in results:
        title = movie.get("title", "Untitled")
        year = movie.get("release_date", "N/A")[:4]
        overview = movie.get("overview", "No description available.")
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None


        title = escape_markdown(title, version=2)
        year = escape_markdown(year, version=2)
        overview = escape_markdown(overview, version=2)

        text = f"*{title}* \\({year}\\)\n_{overview}_"
        recommendations.append((text, poster_url))
    return recommendations

# genre id
def extract_genre_ids(prompt):
    prompt = prompt.lower()
    genre_ids = []

    for keyword, genre_id in GENRE_MAP.items():
        if keyword in prompt:
            genre_ids.append(str(genre_id))

    return ','.join(genre_ids)

# recommendations
def get_recommendations(prompt):
    genre_id = extract_genre_ids(prompt)
    try:
        if genre_id:
            url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc"
        else:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={prompt}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])[:5]
        return format_movies(results)
    except Exception as e:
        print(f"Error in get_recommendations: {e}")
        return []

#  random movie
def get_random_movie():
    try:
        page = random.randint(1, 500)
        url = f"https://api.themoviedb.org/3/discover/movie?api_key={TMDB_API_KEY}&sort_by=popularity.desc&page={page}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        results = data.get("results", [])
        if results:
            return format_movies([random.choice(results)])
    except Exception as e:
        print(f"Error in get_random_movie: {e}")
    return []


async def handle_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    if not user_input:
        await update.message.reply_text("Please type something to get a movie recommendation.")
        return
    recs = get_recommendations(user_input)
    await send_recommendations(update, recs)

# send response
async def send_recommendations(update: Update, recs):
    if not recs:
        await update.message.reply_text("No recommendations found. Try again later.")
        return
    for text, poster_url in recs:
        if poster_url:
            await update.message.reply_photo(photo=poster_url, caption=text, parse_mode="MarkdownV2")
        else:
            await update.message.reply_text(text, parse_mode="MarkdownV2")

# /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a movie name or genre, and I'll recommend something!\nTry /random for a surprise movie!")

# /random 
async def random_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recs = get_random_movie()
    await send_recommendations(update, recs)


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('random', random_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt))
    
    print("Bot is running...")
    app.run_polling()
