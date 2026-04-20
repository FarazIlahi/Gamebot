from bot.bot import run_discord_bot
from database.init_db import init_db

if __name__ == '__main__':
	init_db()
	run_discord_bot()