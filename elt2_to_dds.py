import psycopg2
import hashlib
from datetime import datetime

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "mysecretpassword",
    "host": "127.0.0.1",
    "port": 5433
}

def compute_md5(*values):
    concatenated = '|'.join(str(v) for v in values)
    return hashlib.md5(concatenated.encode('utf-8')).hexdigest()

def load_dds():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, user_id, title, body, source_system, load_ts
        FROM stg.posts
        ORDER BY id
    """)
    rows = cur.fetchall()

    for row in rows:
        post_id, user_id, title, body, source_sys, load_ts = row
        post_hk = compute_md5('POST', post_id)
        user_hk = compute_md5('USER', user_id)
        link_hk = compute_md5(post_hk, user_hk)
        sat_hash = compute_md5(title, body)
        cur.execute("""
            INSERT INTO dds.hub_post (post_hk, post_id, load_ts, source_system)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (post_hk) DO NOTHING
        """, (post_hk, post_id, load_ts, source_sys))
        cur.execute("""
            INSERT INTO dds.hub_user (user_hk, user_id, load_ts, source_system)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_hk) DO NOTHING
        """, (user_hk, user_id, load_ts, source_sys))
        cur.execute("""
            INSERT INTO dds.link_post_user (link_hk, post_hk, user_hk, load_ts, source_system)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (link_hk) DO NOTHING
        """, (link_hk, post_hk, user_hk, load_ts, source_sys))
        cur.execute("""
            INSERT INTO dds.sat_post (post_hk, title, body, hash_diff, load_ts, source_system, effective_ts)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_hk, hash_diff) DO NOTHING
        """, (post_hk, title, body, sat_hash, load_ts, source_sys, load_ts))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Загружено {len(rows)} записей в слой DDS")

if __name__ == "__main__":
    load_dds()