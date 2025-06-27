import random
import discord
from discord import ApplicationContext as Context
from ... import fetch_json, guild_ids, replace_speaker
from discord.ext import commands
import re
from bot.core.core import KitsuneChan
from discord import SlashCommandGroup

roast_langs = {'English': 'en', 'German': 'de', 'Spanish': 'es', 'French': 'fr', 'Russian': 'ru', 'Chinese': 'cn', 'Greek': 'el', 'Swahili': 'sw'}
rizz_langs = ["English", "Spanish", "French", "German", "Italian"]


def setup(bot):
    bot.add_cog(Fun(bot))


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    fun = SlashCommandGroup("fun", "Fun commands")
    slash = fun.command

    # GAYRATE
    @slash(name="gayrate",description="Advanced Gayness measurement protocol", guild_ids=guild_ids)
    @discord.option("user", type=discord.User, description="User to check", required=False)
    async def gayrate(self, ctx: Context, user):
        if user is None:
            await ctx.respond(f"You are {random.randint(0, 100)}% gay.")
        else:
            await ctx.respond(f"{user.name} is {random.randint(0, 100)}% gay.")


    ## VIRGINITY
    @slash(name="virgin", description="Advanced virginity test", guild_ids=guild_ids)
    @discord.option("user", type=discord.User, description="User to check", required=False)
    async def virgin(self, ctx: Context, user):
        choice = random.choice(["virgin", "not virgin"])
        if user is None:
            await ctx.respond(f"You are {choice}.")
        else:
            await ctx.respond(f"{user.name} is {choice}.")


    ## DAILY SCREENTIME
    @slash(name="screentime", type=discord.User, description="Sunrise time", guild_ids=guild_ids)
    @discord.option("user", description="User to check", required=False)
    async def screentime(self, ctx: Context, user):
        random_time = random.randint(0, 24)
        if user is None:
            await ctx.respond(f"Your daily screen time is {random_time} hours.")
        else:
            await ctx.respond(f"{user.name}'s daily screen time is {random_time} hours.")
    

    ## WAIFU
    @slash(name="waifu", description="Count waifus", guild_ids=guild_ids)
    @discord.option("user", type=discord.User, description="User to Count", required=False)
    async def waifu(self, ctx: Context, user):

        rand_value = random.random()
        biased_value = int((1 - rand_value) ** 3 * 50 + 0)
        
        if user is None:
            await ctx.respond(f"You have {biased_value} waifus.")
        else:
            await ctx.respond(f"{user.name} has {biased_value} waifus.")


    ## IQ
    @slash(name="iq", description="Count IQ", guild_ids=guild_ids)
    @discord.option("user", type=discord.User, description="User to Count", required=False)
    async def iq(self, ctx: Context, user):
        rand_value = random.random()
        biased_value = int((1 - rand_value) ** 6 * (200 - 90) + 90)
        if user is None:
            await ctx.respond(f"You have {biased_value} IQ.")
        else:
            await ctx.respond(f"{user.name} has {biased_value} IQ.")


    ## DECIDE
    @slash(name="decide", description="Decide between two options", guild_ids=guild_ids)
    async def decide(self, ctx: Context, first: str, second: str):
        choice = random.choice([first, second])
        modified_choice = replace_speaker(choice)

        common_prefixes = ['should i', 'i', 'or']
        for prefix in common_prefixes:
            modified_choice = re.sub(f'^{prefix}\\s*', '', modified_choice, flags=re.IGNORECASE)

        common_suffixes = ['.', '!', '?', ';']
        modified_choice = re.sub(f'[{re.escape("".join(common_suffixes))}]+$', '', modified_choice)

        await ctx.respond(f"You should {modified_choice}.")


    ## ROAST
    @slash(name="roastme", description="Roast me", guild_ids=guild_ids)
    @discord.option("language", description="Language to get insulted with", required=False, choices=roast_langs.keys())
    async def roastme(self, ctx:Context, language:str):
        await ctx.defer()
        url = f"https://evilinsult.com/generate_insult.php?lang={roast_langs[language]}&type=json"
        response:dict = await fetch_json(url)
        if not "error" in response.keys():
            insult = response['insult']
            await ctx.respond(insult)
        else:
            await ctx.respond(f"Failed to fetch a roast. `{response['error']}` Try again later.")


    @slash(name="rizzme", description="Get a random pickup line", guild_ids=guild_ids)
    @discord.option("language", description="Language to get rizzled in", required=False, choices=rizz_langs)
    async def rizzme(self, ctx:discord.ApplicationContext, language:str = "English"):
        await ctx.defer()
        url = f"https://rizzapi.vercel.app/random?language={language.lower()}"

        response = await fetch_json(url)

        if response is None:
            await ctx.respond("Failed to fetch a pickup line. Try again later.")
        elif "error" in response.keys():
            await ctx.respond(f"Failed to fetch a pickup line. `{response['error']}` Try again later.")
        else:
            pickup_line = response['text']
            await ctx.respond(pickup_line)