from urllib import response

import discord
from discord.ext import commands
import responses
from dotenv import load_dotenv
import os
from google import genai

async def send_message(ctx, user_message):
	try:
		response = responses.handle_response(user_message)
		await ctx.channel.send(response)


	except Exception as e:
		print(e)




def run_discord_bot():
	load_dotenv()
	TOKEN = os.getenv('DISCORD_BOT_TOKEN')
	GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
	client = genai.Client()
	response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Reply in one sentence: say hello like a funny Discord bot."
	)

	print(response.text)
	
	deleted_messages = {}
	cmd_prefix = '.'
	intents = discord.Intents.default()
	intents.typing = True  
	intents.presences = True
	intents.message_content = True  
	intents.members = True
	bot = commands.Bot(command_prefix=cmd_prefix, intents = intents)
	


	@bot.event
	async def on_ready():
		print(f'{bot.user} is now running')

	@bot.event
	async def on_message(message):
		if(str(message.content)[0] == cmd_prefix):
			await bot.process_commands(message)
			return
		if message.author == bot.user:
			return
		user_message = str(message.content)
		await send_message(message, user_message)
		

	@bot.event
	async def on_message_delete(message):
		deleted_messages[message.channel.id] = {
		'content': message.content,
		'author': message.author.name,
		'timestamp':message.created_at
		}
	
	@bot.event
	async def on_member_join(member):
		if member.guild.system_channel:
			await member.guild.system_channel.send("yo wsg new guy")
		print(member.guild.system_channel)

	@bot.event
	async def on_member_remove(member):
		if member.guild.system_channel:
			await member.guild.system_channel.send("man gtfo of here\nWe didnt want you here anyways " + str(member.name))
		print(member.guild.system_channel)


	@bot.command()
	async def pfp(ctx, user: discord.Member = None):	

		if user is None:
			user = ctx.message.author

		if(user == None):
			print("no user")
		avatar_url = user.avatar.url

		await ctx.channel.send(f"{user.mention}'s profile picture: {avatar_url}")


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
	async def snipe(ctx):
		channel_id = ctx.channel.id
		if channel_id in deleted_messages:
			deleted_message = deleted_messages[channel_id]
			await ctx.send(f"Last deleted message by {deleted_message['author']}: {deleted_message['content']}")

		else:
			await ctx.send(f'No deleted messages to snipe')


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

	

		


	bot.run(TOKEN)