from typing import cast
from discord.ui import View, Button, button

from discord import Member, User, Interaction
from discord import ButtonStyle
from discord import InteractionMessage


defaultStyle = ButtonStyle.secondary

class TTTView(View):
    def __init__(self, player:Member|User, opponent:Member|User):
        super().__init__(timeout=30)
        self.opponent:Member|User = opponent
        self.player:Member|User = player
        self.playerTurn = True
        self.message = None
        self.board:list = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]


    def checkWinner(self) -> None:
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        return None


    async def on_timeout(self):
        if self.message:
            await self.message.edit(view=self)
            self.disable_all_items()
            await self.message.channel.send("Game timed out.")


    async def updateGrid(
        self,
        button: Button,
        interaction: Interaction,
        row: int,
        column: int,
    ):
        x = row - 1
        y = column - 1

        if self.board[x][y] is not None:
            await interaction.response.send_message("That spot is already taken!")
            return
        
        if interaction.user == self.player and self.playerTurn:
            button.label = "O"
            button.style = ButtonStyle.success
            self.board[x][y] = True
            self.playerTurn = False
            await interaction.response.defer()
        elif interaction.user == self.opponent and not self.playerTurn:
            button.style = ButtonStyle.primary
            button.label = "X"
            self.board[x][y] = False
            self.playerTurn = True
            await interaction.response.defer()
        else:
            await interaction.response.send_message("It's not your turn!")
            return

        message = cast(InteractionMessage, self.message)
        
        await message.edit(view=self)

        if self.checkWinner() == True:
            await message.edit(content=f"{self.player.mention} won against {self.opponent.mention}", view=self)
            self.disable_all_items()
            self.stop()
        elif self.checkWinner() == False:
            await message.edit(content=f"{self.opponent.mention} won against {self.player.mention}", view=self)
            self.disable_all_items()
            self.stop()
        elif all(all(x is not None for x in row) for row in self.board):
            await message.edit(content="It's a tie!",view=self)
            self.disable_all_items()
            self.stop()
            
        
    async def interaction_check(self, interaction: Interaction) -> bool:
        return bool(interaction.user == self.opponent or interaction.user == self.player)


    @button(label="\u200B", style=defaultStyle, row=0)
    async def one(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 1, 1)

    @button(label="\u200B", style=defaultStyle, row=0)
    async def two(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 1, 2)

    @button(label="\u200B", style=defaultStyle, row=0)
    async def three(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 1, 3)


    @button(label="\u200B", style=defaultStyle, row=1)
    async def four(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 2, 1)

    @button(label="\u200B", style=defaultStyle, row=1)
    async def five(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 2, 2)

    @button(label="\u200B", style=defaultStyle, row=1)
    async def six(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 2, 3)


    @button(label="\u200B", style=defaultStyle, row=2)
    async def seven(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 3, 1)

    @button(label="\u200B", style=defaultStyle, row=2)
    async def eight(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 3, 2)

    @button(label="\u200B", style=defaultStyle, row=2)
    async def nine(self, button:Button, interaction:Interaction):
        await self.updateGrid(button, interaction, 3, 3)
