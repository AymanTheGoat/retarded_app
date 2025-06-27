import asyncio
import asyncpg
import dotenv
import os
import fun.games as x
import pprint 


dotenv.load_dotenv()

user = str(os.getenv('DB_USER'))
database = str(os.getenv('DB_DATABASE'))
password = str(os.getenv('DB_PASSWORD'))
host = str(os.getenv('DB_HOST'))


# Database connection and query example using asyncpg
async def run():
    pool:asyncpg.Pool = await asyncpg.create_pool(
        host=host,
        database=database,
        user=user,
        password=password,
    )
    
    user_id = 1
    score = 100

    async with pool.acquire() as conn: 
        await x.updateSnakePB(conn=conn, user_id=user_id, score=score)
        res = await x.getSnakeStats(conn=conn, user_id=user_id)
        pprint.pprint(res)
    
    # for value in values:
    #     print(value)

    await pool.close()

asyncio.run(run())