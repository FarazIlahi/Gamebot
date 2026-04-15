import discord

def register_moderation_commands(bot):
	@bot.command()
	async def mute(ctx, member: discord.Member = None):
		try:
			if ctx.author.guild_permissions.manage_roles:
				mute_role = discord.utils.get(ctx.guild.roles, name='Muted')
				reg_role = discord.utils.get(ctx.guild.roles, name='reg')

				if not mute_role:
					mute_role = await ctx.guild.create_role(name='Muted', reason='Creating mute role')

				await member.add_roles(mute_role, reason='Muted by command')
				await member.remove_roles(reg_role, reason='Muted by command')

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
				reg_role = discord.utils.get(ctx.guild.roles, name='reg')

				if(mute_role):
					await member.remove_roles(mute_role, reason='Unmuted by command')
					await member.add_roles(reg_role, reason='Unmuted by command')

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
			

    