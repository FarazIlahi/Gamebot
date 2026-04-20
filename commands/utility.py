import discord
from discord import user
from database.repositories.roles_repo import get_all_custom_color_roles_creator, get_all_roles
from database.repositories.users_repo import get_all_users


def register_utility_commands(bot, deleted_messages):
    @bot.command()
    async def pfp(ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed()
        embed.set_image(url=user.avatar.url)
        await ctx.send(embed=embed)

    @bot.command()
    async def snipe(ctx):
        channel_id = ctx.channel.id
        if channel_id in deleted_messages:
            deleted_message = deleted_messages[channel_id]
            await ctx.send(
                f"Last deleted message by {deleted_message['author']}: "
                f"{deleted_message['content']}"
            )
        else:
            await ctx.send("No deleted messages to snipe")

    

    @bot.command()
    async def help(ctx):
        msg = "**Commands:**\n"
        for command in bot.commands:
            if not command.hidden:
                msg += f".{command.name}\n"
        await ctx.send(msg)

    @bot.command()
    async def people(ctx):
        await ctx.send(get_all_users())

    @bot.command()
    async def colorroles(ctx):
        await ctx.send(get_all_custom_color_roles_creator(ctx.guild.id))

    @bot.command()
    async def allroles(ctx):
        await ctx.send([ctx.guild.get_role(int(role_id)).name for role_id in get_all_roles(ctx.guild.id)])

