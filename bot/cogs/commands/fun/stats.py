from discord.ext import commands
from discord import ApplicationContext as Context
import discord
from bot.core.core import KitsuneChan
from bot.core.embed import KitsuneEmbed as Embed 
from ... import guild_ids
from database.fun.games import getTetrisStats
from discord import SlashCommandGroup

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot

    stats = SlashCommandGroup("stats", "Get user stats")
    slash = stats.command
    @slash(name="tetstats", description="Get player's stats.")
    async def tetstats(self, ctx: Context, user: discord.User):
        """Get Tetris stats for a user."""
        if user is None:
            user = ctx.author
        
        async with self.bot.db.acquire() as conn:
            stats = await getTetrisStats(conn, user.id)

        if not stats:
            await ctx.respond(f"No Tetris stats found for {user.mention}.")
            return
        
        dtimestamp = f'<t:{stats["highest_score_time"]}:f>'

        embed = Embed(title=f"Tetris Stats for {user.name}",description="", color=discord.Color.blue())
        embed.add_field(name="Highest Score", value=stats["highest_score"], inline=False)
        embed.add_field(name="Highest Score Time", value=dtimestamp, inline=False)
        embed.add_field(name="Games Played", value=stats["games_played"], inline=False)

        await ctx.respond(embed=embed)

def setup(bot) -> None:
    bot.add_cog(Stats(bot))