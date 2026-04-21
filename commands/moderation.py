import discord

from database.repositories.guilds_repo import upsert_guild
from database.repositories.users_repo import upsert_user

def register_moderation_commands(bot):
	@bot.command()
	async def mute(ctx, member: discord.Member = None):
		try:
			if ctx.author.guild_permissions.manage_roles:
				mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
				base_role = discord.utils.get(ctx.guild.roles, name='base aura')

				if not mute_role:
					mute_role = await ctx.guild.create_role(name='Muted', reason='Creating mute role')

				await member.add_roles(mute_role, reason='Muted by command')
				await member.remove_roles(base_role, reason='Muted by command')

				await ctx.send(f'{member.mention} has been muted.')
			else:
				await ctx.send('You do not have the required permissions to use this command.')

		except Exception as e:
			print(e)


	@bot.command()
	async def unmute(ctx, member: discord.Member = None):
		try:
			if ctx.author.guild_permissions.manage_roles:
				mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
				base_role = discord.utils.get(ctx.guild.roles, name='base aura')

				if(mute_role):
					await member.remove_roles(mute_role, reason='Unmuted by command')
					await member.add_roles(base_role, reason='Unmuted by command')

					await ctx.send(f'{member.mention} has been unmuted')
			else:
				await ctx.send(f'You do not have the required permissions to use this command.')

		except Exception as e:
			print(e)


	@bot.command()
	async def purge(ctx, amount: int):
		if not ctx.author.guild_permissions.manage_messages:
			await ctx.send("You cant do that goofy")
			return

		if amount <=0:
			await ctx.send("bruh")
			return

		if amount > 100:
			await ctx.send("TOO MUCH BETA")
			return

		deleted = await ctx.channel.purge(limit = amount + 1)
		await ctx.send(f"Deleted {len(deleted) - 1} chats.")
			

	@bot.command()
	async def syncusers(ctx):
		guild = ctx.guild

		added = 0

		for member in guild.members:
			if member.bot:
				continue

			upsert_user(member)
			added += 1

		await ctx.send(f"Sync complete. Added {added} users.")

	@bot.command()
	async def syncguild(ctx):
		upsert_guild(ctx.guild)

    