import requests
import psycopg2
import hashlib
from datetime import datetime

API_URL = "https://jsonplaceholder.typicode.com/posts"
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "127.0.0.1",
    "port": 5433
}

def init_db():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS stg;
        CREATE TABLE IF NOT EXISTS stg.posts (
            id INTEGER,
            user_id INTEGER,
            title TEXT,
            body TEXT,
            load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_system VARCHAR(50) DEFAULT 'jsonplaceholder',
            hash_diff VARCHAR(32)
        );
        CREATE SCHEMA IF NOT EXISTS dds;
        CREATE TABLE IF NOT EXISTS dds.hub_post (
            post_hk CHAR(32) PRIMARY KEY,
            post_id INTEGER NOT NULL,
            load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_system VARCHAR(50)
        );
        CREATE TABLE IF NOT EXISTS dds.hub_user (
            user_hk CHAR(32) PRIMARY KEY,
            user_id INTEGER NOT NULL,
            load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_system VARCHAR(50)
        );
        CREATE TABLE IF NOT EXISTS dds.link_post_user (
            link_hk CHAR(32) PRIMARY KEY,
            post_hk CHAR(32) NOT NULL,
            user_hk CHAR(32) NOT NULL,
            load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_system VARCHAR(50),
            FOREIGN KEY (post_hk) REFERENCES dds.hub_post(post_hk),
            FOREIGN KEY (user_hk) REFERENCES dds.hub_user(user_hk)
        );
        CREATE TABLE IF NOT EXISTS dds.sat_post (
            post_hk CHAR(32) NOT NULL,
            title TEXT,
            body TEXT,
            hash_diff CHAR(32),
            load_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source_system VARCHAR(50),
            effective_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (post_hk, hash_diff)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Таблицы успешно созданы (или уже существуют)")

def compute_md5(*values):
    concatenated = '|'.join(str(v) for v in values)
    return hashlib.md5(concatenated.encode('utf-8')).hexdigest()

def load_stg():
    response = requests.get(API_URL)
    response.raise_for_status()
    posts = response.json()
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE stg.posts;")
    print("STG очищена")
    insert_sql = """
        INSERT INTO stg.posts (id, user_id, title, body, load_ts, source_system, hash_diff)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    now = datetime.now()
    for p in posts:
        h = compute_md5(p['id'], p['userId'], p['title'], p['body'])
        cur.execute(insert_sql, (
            p['id'], p['userId'], p['title'], p['body'],
            now, 'jsonplaceholder', h
        ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Загружено {len(posts)} записей в stg.posts")

if __name__ == "__main__":
    init_db()
    load_stg()