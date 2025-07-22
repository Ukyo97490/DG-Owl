import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Chargement des variables d'environnement
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DEFAULT_FEED = os.getenv('DEFAULT_RSS_FEED')

# Configuration du bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Chargement des cogs (modules)
async def load_cogs():
    await bot.load_extension('cogs.rss_cog')

@bot.event
async def on_ready():
    print(f'🦉 DG-Owl est opérationnel | {bot.user}')
    await load_cogs()
    print("Modules chargés avec succès")

# Lancement du bot
if __name__ == '__main__':
    bot.run(TOKEN)