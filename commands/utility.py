import discord

def register_utility_commands(bot, deleted_messages):
    @bot.command()
    async def pfp(ctx, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(f"{user.mention}'s profile picture: {user.avatar.url}")

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