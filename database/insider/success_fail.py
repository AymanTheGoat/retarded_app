from asyncpg import Connection


async def getSuccessMessage(conn:Connection, category:str):
    try:
        result = await conn.fetch(
            "SELECT message FROM messages WHERE category = $1 AND type = $2 ORDER BY RANDOM() LIMIT 1;",
            category, "success"
        )
        return result[0]['message']
    except:
        return "Success"


async def getErrorMessage(conn:Connection, category:str):
    try:
        result = await conn.fetch(
            "SELECT message FROM messages WHERE category = $1 AND type = $2 ORDER BY RANDOM() LIMIT 1;",
            category, "error"
        )
        return result[0]['message']
    except:
        return "Error {e}"