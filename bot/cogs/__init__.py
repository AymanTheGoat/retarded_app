import re
import aiohttp
from discord import SlashCommandGroup

# Groups 
# general -> [ping, nitro]
# games -> [tetris, snake, tictactoe]
# moderation -> [ban, kick, mute, unmute, warn, clear]
# owner -> [reload, load, unload, sync, shutdown, parrot, say]
# utility -> [avatar, serverinfo, userinfo, poll, translate, weather]
# fun -> [rizzme, roastme, decide, iq, gayrate, screentime, virgin, waifu]

# economy -> [balance, daily, pay, profile, shop, slots, work]
# music -> [play, pause, resume, stop, skip, queue, nowplaying]



# general = SlashCommandGroup("general", "General commands like ping, nitro")
g = SlashCommandGroup("game", "Various greeting from cogs!")











guild_ids = ["1353377404760096859"]


def replace_speaker(text: str) -> str:
    """Replaces first-person references with second-person equivalents."""
    replacements = {
        r' I ': 'you',
        r' me ': 'you',
        r' my ': 'your',
        r' mine ': 'yours',
        r'myself': 'yourself',
        r' am ': 'are',
        r' was ': 'were',
        r' we ': 'you all',
        r' us ': 'you all',
        r' our ': 'your',
        r' ours ': 'yours',
        r'ourselves': 'yourselves',
        r'I\'m': "you're",
        r'I\'ve': "you've",
        r'I\'d': "you'd",
        r'I\'ll': "you'll",
        r'we\'re': "you're all",
        r'we\'ve': "you've all",
        r'we\'ll': "you all will",
        r'we\'d': "you all would",
        r'fms': "fys",
    }

    def replacement_func(match):
        word = match.group(0)
        return replacements.get(word.lower(), word)

    pattern = re.compile('|'.join(replacements.keys()), re.IGNORECASE)
    return pattern.sub(replacement_func, text) # type: ignore


async def fetch_json(url) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            return {"error": str(e)}
        


