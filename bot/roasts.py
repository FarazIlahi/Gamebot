import bot.llm as llm
def get_roast(member) -> str:
	return llm.generate_roast(member)
	