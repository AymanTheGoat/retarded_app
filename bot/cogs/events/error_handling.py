
from discord.ext import commands
import discord
from bot.core.core import KitsuneChan
from discord import ApplicationContext as Context

def setup(bot):
    bot.add_cog(ErrorHandler(bot))


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot


    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: Context, error: discord.DiscordException):
        error_message = f"```ansi\n[2;31m[1;31mError[0m[2;31m[0m:\n{error}\n```"
        await ctx.respond(error_message)