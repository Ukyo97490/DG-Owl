import os
import json
import discord
from discord.ext import tasks, commands
import feedparser
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

RSS_FEEDS = [
    "https://korben.info/feed",
    "https://www.clubic.com/rss",
    "https://www.lemondeinformatique.fr/flux-rss/thematique/rss.xml"
]

HISTORY_FILE = "posted.json"

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

async def fetch_and_post_news():
    channel = bot.get_channel(CHANNEL_ID)
    history = load_history()

    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            continue
        latest = feed.entries[0]
        link = latest.link

        if history.get(feed_url) == link:
            continue

        await channel.send(f"📰 **{latest.title}**\n{link}")

        history[feed_url] = link
        save_history(history)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    fetch_news.start()

@tasks.loop(minutes=60)
async def fetch_news():
    await fetch_and_post_news()

@bot.command(name="veille")
async def veille_refresh(ctx, arg=None):
    if arg == "refresh":
        await ctx.send("🔄 Mise à jour manuelle en cours...")
        await fetch_and_post_news()
        await ctx.send("✅ Mise à jour terminée !")
    else:
        await ctx.send("Commande invalide. Utilisez `!veille refresh` pour mettre à jour.")

bot.run(TOKEN)
