import discord
import roasts
from urllib.parse import urlparse

def is_valid_url(url: str):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def is_youtube_url(url: str):
    parsed = urlparse(url)
    return "youtube.com" in parsed.netloc or "youtu.be" in parsed.netloc

def register_fun_commands(bot):
    @bot.command()
    async def roast(ctx, user: discord.Member = None):
        user = user or ctx.author
        msg = await ctx.send("thinking...")
        roast_message = roasts.get_roast(user)
        await msg.edit(content=roast_message)


    @bot.command()
    async def embed(ctx, url: str):
        if not is_valid_url(url):
            await ctx.send("BAD URL.")
            return 
        if not is_youtube_url(url):
            await ctx.send("ONLY YOUTUBE LINKS ARE ALLOWED.")
            return

        try:
            embed = discord.Embed(
                title="Watch this",
                description="Cool video",
                url=url
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send("❌ Something went wrong.")
            print(e)