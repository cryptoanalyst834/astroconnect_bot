import os
import asyncpg

DATABASE_URL = os.getenv("DATABASE_URL")


async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
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
            sun TEXT,
            ascendant TEXT
        );
    """)
    await conn.close()


async def save_user(data):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO users (
            telegram_id, name, gender, birth_date, birth_time, birth_city,
            location_city, looking_for, about, photo, sun, ascendant
        ) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
        ON CONFLICT (telegram_id) DO UPDATE SET
            name = EXCLUDED.name,
            gender = EXCLUDED.gender,
            birth_date = EXCLUDED.birth_date,
            birth_time = EXCLUDED.birth_time,
            birth_city = EXCLUDED.birth_city,
            location_city = EXCLUDED.location_city,
            looking_for = EXCLUDED.looking_for,
            about = EXCLUDED.about,
            photo = EXCLUDED.photo,
            sun = EXCLUDED.sun,
            ascendant = EXCLUDED.ascendant;
    """, data["telegram_id"], data["name"], data["gender"],
         data["birth_date"], data["birth_time"], data["birth_city"],
         data["location_city"], data["looking_for"], data["about"],
         data["photo"], data["sun"], data["ascendant"])
    await conn.close()


async def get_user(telegram_id):
    conn = await asyncpg.connect(DATABASE_URL)
    result = await conn.fetchrow("SELECT * FROM users WHERE telegram_id = $1", telegram_id)
    await conn.close()
    return result
