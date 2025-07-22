import os
import json
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("Le token Discord n'est pas défini dans les variables d'environnement !")

try:
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except (TypeError, ValueError):
    raise ValueError("CHANNEL_ID invalide ou manquant dans les variables d'environnement !")

# Fichier pour stocker l'historique des liens postés
HISTORY_FILE = "history.json"

# Charger l'historique existant ou initialiser
try:
    with open(HISTORY_FILE, "r") as f:
        posted_links = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    posted_links = []

intents = discord.Intents.default()
intents.message_content = True  # Obligatoire pour lire le contenu des messages
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connecté en tant que {bot.user}")


@bot.command(name="veille", help="Poster un lien si nouveau dans le channel veille technologique")
async def veille(ctx, url: str):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("Cette commande ne fonctionne que dans le bon channel.")
        return

    if url in posted_links:
        await ctx.send("Ce lien a déjà été posté.")
        return

    posted_links.append(url)
    with open(HISTORY_FILE, "w") as f:
        json.dump(posted_links, f, indent=2)

    await ctx.send(f"Nouvelle veille ajoutée : {url}")


bot.run(TOKEN)
