import os
import asyncpg
import asyncio

DATABASE_URL = os.getenv("DATABASE_URL")

CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT PRIMARY KEY,
    name TEXT,
    gender TEXT,
    birth_date TEXT,
    birth_time TEXT,
    birth_city TEXT,
    location_city TEXT,
    looking_for TEXT,
    about TEXT,
    photo TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);
"""

async def connect():
    return await asyncpg.connect(DATABASE_URL)

async def init_db():
    conn = await connect()
    await conn.execute(CREATE_USERS_TABLE)
    await conn.close()

async def save_user(data):
    conn = await connect()
    await conn.execute("""
        INSERT INTO users (telegram_id, name, gender, birth_date, birth_time, birth_city,
                           location_city, looking_for, about, photo)
        VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
        ON CONFLICT (telegram_id) DO UPDATE
        SET name=$2, gender=$3, birth_date=$4, birth_time=$5, birth_city=$6,
            location_city=$7, looking_for=$8, about=$9, photo=$10;
    """, data["telegram_id"], data["name"], data["gender"], data["birth_date"],
         data["birth_time"], data["birth_city"], data["location_city"],
         data["looking_for"], data["about"], data.get("photo", ""))
    await conn.close()

async def get_user(telegram_id):
    conn = await connect()
    row = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
    await conn.close()
    return row
