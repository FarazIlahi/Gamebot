import discord
import roasts

def register_fun_commands(bot):
    @bot.command()
    async def roast(ctx, user: discord.Member = None):
        user = user or ctx.author
        roast_message = roasts.get_roast(user)
        await ctx.send(roast_message)