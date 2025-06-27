from discord import ApplicationContext, Member, option
from discord.ext import commands
from bot.core.core import KitsuneChan
from pycord.multicog import subcommand
from logic.games.tictactoe import TTTView


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot
        self.current_player = None

    
    @subcommand("game", independent=True) # type: ignore
    @commands.slash_command(name="tictactoe", description="Start a game of Tic-Tac-Toe")
    @option("opponent", desription="Who you want to play against", required=True)
    async def tictactoe(self, ctx:ApplicationContext, opponent:Member):
        view = TTTView(ctx.author, opponent)
        await ctx.respond(f'You are now playing against {opponent.mention}.', view=view)
        view.message = await ctx.interaction.original_response()


def setup(bot:KitsuneChan):
    bot.add_cog(TicTacToe(bot))