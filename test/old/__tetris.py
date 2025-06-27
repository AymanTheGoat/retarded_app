from discord import ApplicationContext
from discord.ext import commands
from random import choice
from bot.core.core import KitsuneChan
from bot.core.embed import KitsuneEmbed as Embed
from pycord.multicog import subcommand
from logic.games.tetris import TetrisPiece, Board, TetrisView
from discord.ext.commands import Cog



class Tetris(Cog):
    def __init__(self, bot):
        self.bot:KitsuneChan = bot


    @subcommand("game", independent=True) # type: ignore
    @commands.slash_command(name="tetris", description="Play Tetris")
    async def tetris(self, ctx: ApplicationContext) -> None:
        board = Board()
        board.spawnPiece(choice(list(TetrisPiece.shapes.keys())))
        
        embed = Embed(
            title="Tetris",
            description=board.format(),
            color=0xBEBEFE
        )

        embed.add_field(name="Score", value=str(board.score))
        
        view = TetrisView(self.bot, board, ctx.author.id)
        await ctx.respond(embed=embed, view=view)
        view.message = await ctx.interaction.original_response()



def setup(bot) -> None:
    bot.add_cog(Tetris(bot))
