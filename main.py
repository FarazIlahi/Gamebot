import bot.bot as bot
from database import init_db

if __name__ == '__main__':
	init_db()
	bot.run_discord_bot()