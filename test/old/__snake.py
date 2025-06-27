
from discord import Color, ApplicationContext
from discord.ext import commands
from discord import SlashCommandGroup
from bot.core.core import KitsuneChan
from bot.core.embed import KitsuneEmbed as Embed
from logic.games.snake import Snake, SnakeView




class SnakeCog(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot
        self.current_player = None
    
    game = SlashCommandGroup("game", "Games commands")

    @game.command(name="snake", description="Start a game of Snake")
    async def snake(self, ctx:ApplicationContext):
        self.current_player = ctx.author
        snake = Snake()
        view = SnakeView(self.bot, snake, ctx.author.id)
        embed = Embed(
            title="Snake",
            description=snake.format(),
            color=Color.random()
        )
        await ctx.respond("Snaking...", embed=embed, view=view)
        view.message = await ctx.interaction.original_response()


def setup(bot):
    bot.add_cog(SnakeCog(bot))

