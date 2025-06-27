import asyncpg, os
from discord.ext import commands
from discord import Interaction
from database.insider.success_fail import getSuccessMessage
import time
from pycord.multicog import Bot

class KitsuneChan(Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db:asyncpg.Pool = None # type: ignore
    
    async def create_db_pool(self):
        start = time.perf_counter()
        self.db = await asyncpg.create_pool(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE'),
            port=os.getenv('DB_PORT'),
        )
        end = time.perf_counter()
        print(f"Database connect in {(end-start)*1000:.2f}ms")

    async def success(self, interaction:Interaction, type_, ephemeral:bool):
        async with self.db.acquire() as conn:
            message = await getSuccessMessage(conn=conn, category=type_)
        if message:
            await interaction.response.send_message(message, ephemeral=ephemeral)
        else:
            await interaction.response.send_message("Success!", ephemeral=ephemeral)


    async def error(self):
        # TODO
        ...