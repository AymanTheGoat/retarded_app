from discord.ext import commands
import discord
import datetime
from bot.core.core import KitsuneChan

def setup(bot):
    bot.add_cog(Startup(bot))


class Startup(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    @commands.Cog.listener()
    async def on_ready(self):
        if self.bot.user is None:
            print("Bot user is None. Something went wrong!")
            return
        self.bot.auto_sync_commands = True
        await self.bot.sync_commands()
        await self.bot.create_db_pool()
        bot_name = self.bot.user.name
        bot_id = self.bot.user.id
        pycord_version = discord.__version__
        guild_count = len(self.bot.guilds)
        guild_names = ', '.join(guild.name for guild in self.bot.guilds)
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
    
    # More things like changing presence to be added later
