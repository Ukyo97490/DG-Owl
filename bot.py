import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # Peut être None

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user.name}")

    for guild in bot.guilds:
        channel = None

        # Si CHANNEL_ID est défini
        if CHANNEL_ID:
            try:
                channel = guild.get_channel(int(CHANNEL_ID))
                print(f"📌 Salon trouvé par ID : {channel.name}")
            except Exception as e:
                print(f"⚠️ Erreur lors de la récupération du salon par ID : {e}")

        # Sinon, on tente de le retrouver par nom
        if not channel:
            channel = discord.utils.get(guild.text_channels, name="veille-technologique")
            if channel:
                print(f"📌 Salon trouvé par nom : {channel.name}")
            else:
                # Sinon, on le crée
                print("➕ Création du salon veille-technologique")
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=True)
                }
                channel = await guild.create_text_channel("veille-technologique", overwrites=overwrites)
                print(f"✅ Salon créé : {channel.name} (ID: {channel.id})")

        # Tu peux maintenant poster dans ce salon
        await channel.send("🤖 Le bot est prêt à suivre l'actualité technologique !")

bot.run(TOKEN)
