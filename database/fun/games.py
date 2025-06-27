from asyncpg import Connection


async def updateTetrisPB(conn: Connection, user_id, score):
    try:
        await conn.execute("""
            INSERT INTO tetris_stats (user_id, highest_score, games_played, highest_score_time)
            VALUES ($1, $2, 1, NOW())
            ON CONFLICT (user_id) DO UPDATE
            SET 
                highest_score = GREATEST(tetris_stats.highest_score, EXCLUDED.highest_score),
                games_played = tetris_stats.games_played + 1,
                highest_score_time = CASE 
                    WHEN EXCLUDED.highest_score > tetris_stats.highest_score 
                    THEN NOW() 
                    ELSE tetris_stats.highest_score_time 
                END
        """, user_id, score)
        return None
    except Exception as e:
        return str(e)


async def updateSnakePB(conn: Connection, user_id, score):
    try:
        await conn.execute("""
            INSERT INTO snake_stats (user_id, highest_score, games_played, highest_score_time)
            VALUES ($1, $2, 1, NOW())
            ON CONFLICT (user_id) DO UPDATE
            SET 
                highest_score = GREATEST(snake_stats.highest_score, EXCLUDED.highest_score),
                games_played = snake_stats.games_played + 1,
                highest_score_time = CASE 
                    WHEN EXCLUDED.highest_score > snake_stats.highest_score 
                    THEN NOW() 
                    ELSE snake_stats.highest_score_time 
                END
        """, user_id, score)
        return None
    except Exception as e:
        return str(e)


async def getTetrisStats(conn:Connection, user_id):
    result = await conn.fetch("""
        SELECT highest_score, highest_score_time, games_played
        FROM tetris_stats
        WHERE user_id = $1
    """, user_id)
    
    record = result[0]

    return {
        "highest_score": record["highest_score"],
        "highest_score_time": int(record["highest_score_time"].timestamp()),
        "games_played": record["games_played"],
    }


async def getSnakeStats(conn:Connection, user_id):
    result = await conn.fetch("""
        SELECT highest_score, highest_score_time, games_played
        FROM snake_stats
        WHERE user_id = $1
    """, user_id)
    
    record = result[0]

    return {
        "highest_score": record["highest_score"],
        "highest_score_time": int(record["highest_score_time"].timestamp()),
        "games_played": record["games_played"],
    }


async def getTetrisLeaderboard(conn: Connection, limit=10):
    result = await conn.fetch("""
        SELECT user_id, highest_score, highest_score_time, games_played
        FROM tetris_stats
        ORDER BY highest_score DESC
        LIMIT $1
    """, limit)
    
    return [
        {
            "user_id": record["user_id"],
            "highest_score": int(record["highest_score_time"].timestamp()),
            "games_played": record["games_played"],
        } for record in result
    ]


async def getSnakeLeaderboard(conn: Connection, limit=10):
    result = await conn.fetch("""
        SELECT user_id, highest_score, highest_score_time, games_played
        FROM snake_stats
        ORDER BY highest_score DESC
        LIMIT $1
    """, limit)
    
    return [
        {
            "user_id": record["user_id"],
            "highest_score": int(record["highest_score_time"].timestamp()),
            "games_played": record["games_played"],
        } for record in result
    ]