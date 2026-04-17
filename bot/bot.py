import discord
from discord.ext import commands
from .config import DISCORD_BOT_TOKEN, GEMINI_API_KEY, COMMAND_PREFIX
from .events import register_events
from commands.utility import register_utility_commands	
from commands.moderation import register_moderation_commands
from commands.fun import register_fun_commands





def run_discord_bot():
	deleted_messages = {}

	intents = discord.Intents.default()
	intents.typing = True  
	intents.presences = True
	intents.message_content = True  
	intents.members = True
	
	bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents = intents)

	register_events(bot, deleted_messages)
	register_utility_commands(bot, deleted_messages)
	register_moderation_commands(bot)
	register_fun_commands(bot)
	
	bot.run(DISCORD_BOT_TOKEN)