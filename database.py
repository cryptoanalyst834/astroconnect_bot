import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def create_users_table():
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
            sun_sign TEXT,
            ascendant TEXT
        )
    """)
    await conn.close()

async def save_user(user_data: dict):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute("""
        INSERT INTO users (telegram_id, name, gender, birth_date, birth_time, birth_city, location_city, looking_for, about, photo, sun_sign, ascendant)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
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
            sun_sign = EXCLUDED.sun_sign,
            ascendant = EXCLUDED.ascendant
    """, user_data["telegram_id"], user_data["name"], user_data["gender"],
         user_data["birth_date"], user_data["birth_time"], user_data["birth_city"],
         user_data["location_city"], user_data["looking_for"], user_data["about"],
         user_data["photo"], user_data["sun_sign"], user_data["ascendant"])
    await conn.close()

async def get_all_users():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch("SELECT * FROM users")
    await conn.close()
    return [dict(row) for row in rows]
