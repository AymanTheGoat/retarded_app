from discord import ApplicationContext, Member, Color, SlashCommandGroup, option
from discord.ext import commands
from random import choice

from bot.core.core import KitsuneChan
from bot.core.embed import KitsuneEmbed as Embed
from logic.games.snake import Snake, SnakeView
from logic.games.tetris import TetrisPiece, Board, TetrisView
from logic.games.tictactoe import TTTView
from ... import guild_ids  # Adjust import path if needed


class GameCog(commands.Cog):
    def __init__(self, bot: KitsuneChan):
        self.bot = bot
        self.current_player = None

    game = SlashCommandGroup("game", "Games commands")

    @game.command(name="snake", description="Start a game of Snake", guild_ids=guild_ids)
    async def snake(self, ctx: ApplicationContext):
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

    @game.command(name="tetris", description="Play Tetris", guild_ids=guild_ids)
    async def tetris(self, ctx: ApplicationContext):
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

    @game.command(name="tictactoe", description="Start a game of Tic-Tac-Toe", guild_ids=guild_ids)
    @option("opponent", description="Who you want to play against", required=True)
    async def tictactoe(self, ctx: ApplicationContext, opponent: Member):
        view = TTTView(ctx.author, opponent)
        await ctx.respond(f'You are now playing against {opponent.mention}.', view=view)
        view.message = await ctx.interaction.original_response()


def setup(bot: KitsuneChan):
    bot.add_cog(GameCog(bot))
