import psycopg2
import os

def connect():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
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
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def save_user(data):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (telegram_id, name, gender, birth_date, birth_time, birth_city,
                           location_city, looking_for, about, photo)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (telegram_id) DO UPDATE
        SET name=EXCLUDED.name, gender=EXCLUDED.gender, birth_date=EXCLUDED.birth_date,
            birth_time=EXCLUDED.birth_time, birth_city=EXCLUDED.birth_city,
            location_city=EXCLUDED.location_city, looking_for=EXCLUDED.looking_for,
            about=EXCLUDED.about, photo=EXCLUDED.photo;
    """, (
        data["telegram_id"], data["name"], data["gender"],
        data["birth_date"], data["birth_time"], data["birth_city"],
        data["location_city"], data["looking_for"], data["about"], data.get("photo", "")
    ))
    conn.commit()
    conn.close()

def get_user(telegram_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
    user = cur.fetchone()
    conn.close()
    return user