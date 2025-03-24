import discord
from discord import Bot
import os, datetime, random
from dotenv import load_dotenv
guild_ids = ["1353377404760096859"]

# print(len("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓"))
# exit()
load_dotenv()
bot:Bot = discord.Bot(description="a bot for discord")
token:str = str(os.getenv('TOKEN'))


@bot.event
async def on_ready():
    if bot.user is None:
        print("Bot user is None. Something went wrong!")
        return
    
    bot_name = bot.user.name
    bot_id = bot.user.id
    pycord_version = discord.__version__
    guild_count = len(bot.guilds)
    guild_names = ', '.join(guild.name for guild in bot.guilds)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(f"""
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  {("🤖 "+bot_name+" is now online!").center(44)} ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
🔹 ID: {bot_id}
🔹 Pycord Version: {pycord_version}
🔹 Connected to {guild_count} server(s)
🔹 Guilds: {guild_names if guild_count <= 5 else f'{guild_count} servers (list omitted)'}
🔹 Time: {timestamp}
""")


@bot.slash_command(name="hello", description="Say hello to the bot", guild_ids=guild_ids)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")
    await bot.sync_commands()


@bot.slash_command(name="bye", description="Say bye to the bot", guild_ids=guild_ids)
async def bye(ctx: discord.ApplicationContext):
    await ctx.respond("Bye!")
    await bot.close()


@bot.slash_command(name="gayrate", description="Advanced Gayness measurement protocol", guild_ids=guild_ids)
async def roll(ctx: discord.ApplicationContext):
    await ctx.respond(f"You are {random.randint(0, 100)}% gay.")


bot.run(token)