from urllib import response
from google.genai.errors import ServerError
from google import genai
from .config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(prompt: str) -> str:
    try:
        response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents=prompt
    )
        return response.text
    except ServerError:
        return "Bruh the AI overloaded because it can't handle how much of a pain you are, try again later."
    except Exception as e:
        print(f"Error generating roast: {e}")
        return "Bruh the AI is having a meltdown because of you, try again later."
    

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
    - Dont use too  many complicated worrdings, make is brainrotted
    - Make sure you include {member.mention} in the roast (e.g. @user) so it feels personal

    Return ONLY the roast.
    """
    return ask_gemini(prompt)
    