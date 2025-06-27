

CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    message TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('success', 'error')),
    weight INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW()
);



CREATE TABLE tetris_stats (
    user_id BIGINT PRIMARY KEY,
    highest_score INT DEFAULT 0,
    highest_score_time TIMESTAMP,
    games_played INT DEFAULT 0
)



CREATE TABLE snake_stats (
    user_id BIGINT PRIMARY KEY,
    highest_score INT DEFAULT 0,
    highest_score_time TIMESTAMP,
    games_played INT DEFAULT 0
)