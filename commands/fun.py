import discord
import bot.roasts as roasts
from database.repositories.roles_repo import upsert_role


def register_fun_commands(bot):
    @bot.command()
    async def roast(ctx, user: discord.Member = None):
        user = user or ctx.author
        msg = await ctx.send("thinking...")
        roast_message = roasts.get_roast(user)
        await msg.edit(content=roast_message)


