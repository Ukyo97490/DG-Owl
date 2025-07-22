import discord
from discord.ext import commands
import feedparser
from bs4 import BeautifulSoup
import aiohttp

class RSSCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rss')
    async def rss_feed(self, ctx, url: str = None):
        """Affiche les derniers articles d'un flux RSS"""
        if url is None:
            url = ctx.bot.default_feed

        try:
            feed = feedparser.parse(url)
            if not feed.entries:
                await ctx.send("❌ Aucun article trouvé dans ce flux.")
                return

            for entry in feed.entries[:3]:
                # Nettoyage du contenu HTML
                soup = BeautifulSoup(entry.description, 'html.parser')
                clean_desc = soup.get_text()[:200] + "..." if soup.get_text() else "Pas de description"

                embed = discord.Embed(
                    title=entry.title[:256],
                    description=clean_desc,
                    url=entry.link,
                    color=0x2ecc71
                )
                embed.set_footer(text=f"Source: {feed.feed.get('title', 'Inconnu')}")
                await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"⚠️ Erreur: {str(e)[:100]}")

async def setup(bot):
    bot.default_feed = os.getenv('DEFAULT_RSS_FEED')
    await bot.add_cog(RSSCog(bot))
