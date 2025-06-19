import os, asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            name TEXT, gender TEXT,
            birth_date TEXT, birth_time TEXT,
            birth_city TEXT, location_city TEXT,
            looking_for TEXT, about TEXT, photo TEXT
        );
    """)
    await conn.close()

async def save_user(data):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(... )  # аналогично предыдущим версиям
    await conn.close()
