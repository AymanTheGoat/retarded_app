import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from bot.core.core import KitsuneChan
 

# Load environment variables
load_dotenv()

TOKEN = os.getenv("TOKEN") or ""

bot = KitsuneChan(
    command_prefix="!",
    intents=discord.Intents.all()
)

# Load cogs
for root, _, files in os.walk("bot/cogs"):
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            cog_path = os.path.join(root, file).replace("/", ".").replace("\\", ".")[:-3]
            try:
                bot.load_extension(cog_path)
                print(f"Loaded cog: {cog_path}")
            except Exception as e:
                print(f"Failed to load {cog_path}: {e}")

# Run the bot
bot.run(TOKEN)