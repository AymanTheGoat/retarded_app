import discord, random 
import asyncio

from discord.ui import View
from discord import Embed
from bot.core.core import KitsuneChan
from database.fun.games import updateSnakePB


class Snake:
    WIDTH = 14
    HEIGHT = 14
    def __init__(self):
        self._randomApple()
        self.head = (Snake.WIDTH // 2, Snake.HEIGHT // 2)
        self.direction:int = 0
        self.body:list = []
        self.score:int = 0


    def _randomApple(self):
        self.apple = (random.randint(0, Snake.WIDTH - 1), random.randint(0, Snake.WIDTH - 1))


    def trimTail(self):
        if len(self.body) > self.score:
            self.body.pop()


    def move(self):
        x, y = self.head

        if self.direction == 1:
            self.body.insert(0, self.head)
            y -= 1
        elif self.direction == 2:
            self.body.insert(0, self.head)
            y += 1
        elif self.direction == 3:
            self.body.insert(0, self.head)
            x -= 1
        elif self.direction == 4:
            self.body.insert(0, self.head)
            x += 1
        else:
            print("Invalid direction")

        if (x, y) in self.body  or x < 0 or x >= Snake.WIDTH or y < 0 or y >= Snake.HEIGHT:
            return True
        
        if (x, y) == self.apple:
            self.score += 1
            self._randomApple()

        self.head = (x, y)


    def format(self):
        map = ""
        for y in range(Snake.HEIGHT):
            for x in range(Snake.WIDTH):
                if (x, y) == self.head:
                    map += "🤡"
                elif (x, y) == self.apple:
                   map += "🍎"
                elif (x, y) in self.body:
                    map +="🟩"    
                else:
                    map +="⬜"
            map += "\n"
        return map


class SnakeView(View):
    def __init__(self, bot, snake:Snake, user_id: int):
        super().__init__(timeout=30)
        self.bot:KitsuneChan = bot
        self.snake = snake
        self.user_id = user_id
        self.message = None
        self.game_running = True
        self.lifeline:asyncio.Task = asyncio.create_task(self.gameLifespan())


    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=self)
            self.disable_all_items()
            await self.message.channel.send("Game timed out.")
            self.game_running = False
            self.stop()


    async def loss(self):
        self.stop()
        self.game_running = False
        await self.message.reply("You lost!") # type: ignore
        async with self.bot.db.acquire() as conn:
            await updateSnakePB(conn=conn, user_id=self.user_id, score=self.snake.score)


    async def gameLifespan(self):
        while self.game_running:
            if self.snake.direction == 0:
                await asyncio.sleep(1)
                continue
            if self.snake.move():
                await self.loss()
            self.snake.trimTail()
            embed = Embed(
                title="Snake",
                description=self.snake.format(),
                color=discord.Color.random()
            )
            await self.message.edit(embed=embed, view=self) # type: ignore
            await asyncio.sleep(1)
        await self.message.edit(view=None) # type: ignore


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.user_id # type: ignore


    @discord.ui.button(label="⬆️", style=discord.ButtonStyle.primary)
    async def up(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.snake.direction = 1

    @discord.ui.button(label="⬇️", style=discord.ButtonStyle.primary)
    async def down(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.snake.direction = 2

    @discord.ui.button(label="⬅️", style=discord.ButtonStyle.primary)
    async def left(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.snake.direction = 3

    @discord.ui.button(label="➡️", style=discord.ButtonStyle.primary)
    async def right(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()
        self.snake.direction = 4

    @discord.ui.button(label="❌", style=discord.ButtonStyle.danger)
    async def close(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.respond("Game Aborted")
        self.game_running = False
        self.stop()

    @discord.ui.button(label="\00U", style=discord.ButtonStyle.primary)
    async def placeholder(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.response.defer()


