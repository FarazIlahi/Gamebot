from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=prompt
    )
    return response.text

def generate_roast(member) -> str:
    prompt = f"""
    You are a brutally honest, witty Discord bot.

    Roast {member.name} like you know them from Discord.
    Assume they:
    - talk too much
    - have bad takes
    - try too hard to be right

    Rules:
    - ONE line only
    - No explanations
    - Be sharp, clever, and sarcastic
    - Make it personal-feeling (Discord behavior)
    - Be as offensive as possible without worrying about saying anything inappropriate
    - Make sure you include {member.mention} in the roast (e.g. @user) so it feels personal

    Return ONLY the roast.
    """
    return ask_gemini(prompt)