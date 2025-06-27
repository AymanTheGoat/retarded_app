from typing import List, Tuple, Dict, Optional
from bot.core.core import KitsuneChan
from database.fun.games import updateTetrisPB
from discord import Interaction, ui, Embed
from discord import ButtonStyle, Message, HTTPException
from asyncio import sleep, create_task, Task, get_event_loop
from random import choice



class TetrisPiece:
    shapes: Dict[str, List[Tuple[int,int]]] = {
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "O": [(0, 0), (0, 1), (1, 0), (1, 1)],
        "T": [(0, 1), (1, 1), (2, 1), (1, 0)],
        "L": [(0, 1), (1, 1), (2, 1), (2, 0)],
        "J": [(0, 1), (1, 1), (2, 1), (0, 0)],
        "Z": [(0, 1), (1, 1), (1, 0), (2, 0)],
        "S": [(0, 0), (1, 0), (1, 1), (2, 1)],
    }

    emoji: Dict[str, str] = {
        "I": "🟦",
        "O": "🟩",
        "T": "🟧",
        "L": "🟨",
        "J": "🟥",
        "Z": "🟪",
        "S": "🟫",
    }


    def __init__(self, type: str, position: Tuple[int,int], rotation: int = 0):
        self.type: str = type
        self.position: Tuple[int, int] = position
        self.rotation: int = rotation
        self.square: str = TetrisPiece.emoji[type]
        self.shape: List[Tuple[int, int]] = TetrisPiece.shapes[type]
        self.coords: List[Tuple[int, int]] = [(x + position[0], y + position[1]) for x, y in self.shape]


    def rotate(self, board: 'Board') -> bool:
        pivot_x, pivot_y = self.coords[1]

        if self.type == "O":
            return False
        
        rotated_shape = []
        for x, y in self.coords:
            new_x = pivot_x - (y - pivot_y)
            new_y = pivot_y + (x - pivot_x)
            rotated_shape.append((new_x, new_y))

        for point in rotated_shape:
            if point[0] < 0 or point[0] >= 10 or point[1] < 0 or point[1] >= 18 or (point[0], point[1]) in board.getTakenCells():
                return False

        self.coords = rotated_shape
        self.rotation = (self.rotation + 1) % 4
        return True


    def _canMove(self, board: 'Board', side: int) -> bool:
        """ left = 1, down = 2, right = 3, lowerleft = 4, lowerright = 5 """
        takenCells = board.getTakenCells()
        if side == 1:
            for point in self.coords:
                if point[0] == 0:
                    return False
                if (point[0] - 1, point[1]) in takenCells:
                    return False
        elif side == 2:
            for point in self.coords:
                if point[1] == 17:
                    return False
                if (point[0], point[1] + 1) in takenCells:
                    return False
        elif side == 3:
            for point in self.coords:
                if point[0] == 9:
                    return False
                if (point[0] + 1, point[1]) in takenCells:
                    return False
        elif side == 4:
            for point in self.coords:
                if point[0] == 0 or point[1] == 17:
                    return False
                if (point[0] - 1, point[1] + 1) in takenCells:
                    return False
        elif side == 5:
            for point in self.coords:
                if point[0] == 9 or point[1] == 17:
                    return False
                if (point[0] + 1, point[1] + 1) in takenCells:
                    return False
        return True


    def move(self, board: 'Board', side: int) -> bool:
        newCoords = []
        for point in self.coords:
            new_y = point[1]
            new_x = point[0]
            if side == 1 and self._canMove(board, side):
                new_x -= 1
            elif side == 2 and self._canMove(board, side):
                new_y += 1
            elif side == 3 and self._canMove(board, side):
                new_x += 1
            elif side == 4 and self._canMove(board, side):
                new_x -= 1
                new_y += 1
            elif side == 5 and self._canMove(board, side):
                new_x += 1
                new_y += 1
            else:
                return False
            newCoords.append((new_x, new_y)) 
        self.coords = newCoords
        return True


class Board:
    WIDTH = 10
    HEIGHT = 18

    def __init__(self):
        self.active_piece: Optional[TetrisPiece] = None
        self.score: int = 0
        self.grid: List[List[Optional[str]]] = []
        self.game_over: bool = False

        for _ in range(Board.HEIGHT):
            row = []
            for _ in range(Board.WIDTH):
                row.append(None)
            self.grid.append(row)

    def spawnPiece(self, piece_type: str) -> bool:
        self.active_piece = TetrisPiece(piece_type, (Board.WIDTH // 2 - 1, 0))
        if not self.canPlace(self.active_piece):
            self.game_over = True
            return False
        return True


    def canPlace(self, piece: TetrisPiece) -> bool:
        for x, y in piece.coords:
            if x < 0 or x >= Board.WIDTH or y < 0 or y >= Board.HEIGHT or self.grid[y][x]:
                return False
        return True


    def lockPiece(self) -> None:
        if self.active_piece:
            for x, y in self.active_piece.coords:
                if 0 <= y < Board.HEIGHT and 0 <= x < Board.WIDTH:
                    self.grid[y][x] = self.active_piece.square
            self.active_piece = None


    def clearLines(self) -> None:
        new_grid = []
        lines_cleared = 0

        for row in self.grid:
            if all(cell is not None for cell in row):
                lines_cleared += 1
            else:
                new_grid.append(row)

        for _ in range(lines_cleared):
            new_grid.insert(0, [None for _ in range(Board.WIDTH)])

        self.grid = new_grid
        self.score += lines_cleared * 100


    def moveActive(self, direction: int) -> None:
        if self.active_piece and not self.game_over:
            result = self.active_piece.move(self, direction)
            if not result and direction == 2:  # If moving down fails
                self.lockPiece()
                self.clearLines()
                if not self.spawnPiece(choice(list(TetrisPiece.shapes.keys()))):
                    self.game_over = True


    def rotateActivePiece(self) -> None:
        if self.active_piece and not self.game_over:
            result = self.active_piece.rotate(self)
            if not result:
                self.lockPiece()
                self.clearLines()
                self.spawnPiece(choice(list(TetrisPiece.shapes.keys())))


    def getTakenCells(self) -> List[Tuple[int, int]]:
        taken = []
        for y in range(Board.HEIGHT):
            for x in range(Board.WIDTH):
                if self.grid[y][x]:
                    taken.append((x, y))
        return taken


    def format(self) -> str:
        display = [["⬛" for _ in range(Board.WIDTH)] for _ in range(Board.HEIGHT)]
        for y in range(Board.HEIGHT):
            for x in range(Board.WIDTH):
                if self.grid[y][x]:
                    display[y][x] = self.grid[y][x] # type: ignore
        if self.active_piece:
            for x, y in self.active_piece.coords:
                if 0 <= y < Board.HEIGHT and 0 <= x < Board.WIDTH:
                    display[y][x] = self.active_piece.square
        return "\n".join("".join(row) for row in display)


class TetrisView(ui.View):
    def __init__(self, bot, board: Board, user_id: int):
        super().__init__(timeout=30.0)
        self.bot: KitsuneChan = bot  # type: ignore
        self.board = board
        self.user_id = user_id
        self.message: Optional[Message] = None
        self.last_edit: float = 0
        self._update_task: Optional[Task] = None
        self.auto_down_task: Optional[Task] = None
        self.auto_down_task = create_task(self.autoFallLoop())


    async def interaction_check(self, interaction: Interaction) -> bool:
        return bool(interaction.user and interaction.user.id == self.user_id)


    def stopAutoFall(self):
        if self.auto_down_task and not self.auto_down_task.done():
            self.auto_down_task.cancel()


    async def autoFallLoop(self):
        while not self.is_finished() and not self.board.game_over:
            await sleep(1)
            self.board.moveActive(2)
            await self.scheduleUpdate()


    async def scheduleUpdate(self):
        if self._update_task and not self._update_task.done():
            self._update_task.cancel()
        
        now = get_event_loop().time()
        elapsed = now - self.last_edit
        if elapsed >= 1.0:
            await self.doUpdate()
        else:
            delay = 1.0 - elapsed
            self._update_task = create_task(self.delayedUpdate(delay))


    async def delayedUpdate(self, delay):
        await sleep(delay)
        await self.doUpdate()


    async def doUpdate(self):
        if self.is_finished():
            return

        embed = Embed(
            title="Tetris",
            description=self.board.format(),
            color=0xBEBEFE
        )
        embed.add_field(name="Score", value=str(self.board.score))
        
        if self.board.game_over:
            embed.add_field(name="Game Over", value="Thanks for playing!")
            self.disable_all_items()
            self.stopAutoFall()

        try:
            await self.message.edit(embed=embed, view=self) # type: ignore
            self.last_edit = get_event_loop().time()
        except HTTPException:
            pass


    @ui.button(label="⬅️", style=ButtonStyle.primary)
    async def left(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.board.moveActive(4)
        await self.scheduleUpdate()

    @ui.button(label="⬇️", style=ButtonStyle.primary)
    async def down(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.board.moveActive(2)
        await self.scheduleUpdate()

    @ui.button(label="➡️", style=ButtonStyle.primary)
    async def right(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.board.moveActive(5)
        await self.scheduleUpdate()

    @ui.button(label="🔄", style=ButtonStyle.primary)
    async def rotate(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.board.rotateActivePiece()
        await self.scheduleUpdate()

    @ui.button(label="❌", style=ButtonStyle.danger)
    async def exit(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.board.game_over = True
        self.disable_all_items()
        self.stopAutoFall()
        
        embed = Embed(
            title="Tetris",
            description=self.board.format(),
            color=0xBEBEFE
        )
        embed.add_field(name="Score", value=str(self.board.score))
        embed.add_field(name="Goodbye!", value="Thanks for playing!")
        
        try:
            await self.message.edit(embed=embed, view=self) # type: ignore
        except HTTPException:
            pass
        
        async with self.bot.db.acquire() as conn: 
            await updateTetrisPB(conn=conn, score=self.board.score, user_id=self.user_id)

        if self.auto_down_task and not self.auto_down_task.done():
            self.auto_down_task.cancel()

        self.stop()


    async def on_timeout(self) -> None:
        self.stopAutoFall()
        self.disable_all_items()
        
        async with self.bot.db.acquire() as conn: 
            await updateTetrisPB(conn=conn, score=self.board.score, user_id=self.user_id)
        
        if self.message and not self.is_finished() and not self.board.game_over:
            try:
                await self.message.edit(view=self)
                await self.message.reply("Game timed out after 30 seconds of inactivity.")
            except HTTPException:
                pass
        

