import sqlite3
import random
from datetime import datetime
from faker import Faker

fake = Faker()


def create_connection(db_name="social.db"):
    conn = sqlite3.connect(db_name)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(50) NOT NULL UNIQUE,
        role VARCHAR(50) NOT NULL,
        created_on DATETIME NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content VARCHAR(255) NOT NULL,
        user_id INTEGER NOT NULL,
        deleted BOOLEAN NOT NULL DEFAULT 0,
        created_on DATETIME NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS follows (
        following_user_id INTEGER NOT NULL,
        followed_user_id INTEGER NOT NULL,
        PRIMARY KEY (following_user_id, followed_user_id),
        FOREIGN KEY (following_user_id) REFERENCES users(id),
        FOREIGN KEY (followed_user_id) REFERENCES users(id)
    );
    """)

    conn.commit()


def insert_spoof_data(conn):
    cursor = conn.cursor()

    # --------------------
    # USERS (~20)
    # --------------------
    roles = ["admin", "user", "moderator"]
    users = []

    for _ in range(20):
        users.append((
            fake.unique.user_name(),
            random.choice(roles),
            fake.date_time_between(start_date="-2y", end_date="now").isoformat()
        ))

    cursor.executemany("""
    INSERT INTO users (username, role, created_on)
    VALUES (?, ?, ?);
    """, users)

    cursor.execute("SELECT id FROM users;")
    user_ids = [row[0] for row in cursor.fetchall()]

    # --------------------
    # POSTS (~30)
    # --------------------
    posts = []

    for _ in range(200):
        posts.append((
            fake.sentence(nb_words=15),
            random.choice(user_ids),
            random.choice([0, 0, 0, 0, 0, 1]),  # mostly not deleted
            fake.date_time_between(start_date="-1y", end_date="now").isoformat()
        ))

    cursor.executemany("""
    INSERT INTO posts (content, user_id, deleted, created_on)
    VALUES (?, ?, ?, ?);
    """, posts)

    # --------------------
    # FOLLOWS (~50)
    # --------------------
    follows = set()

    while len(follows) < 300:
        follower = random.choice(user_ids)
        followed = random.choice(user_ids)

        if follower != followed:
            follows.add((follower, followed))

    cursor.executemany("""
    INSERT INTO follows (following_user_id, followed_user_id)
    VALUES (?, ?);
    """, list(follows))

    conn.commit()


def main():
    conn = create_connection()
    create_tables(conn)
    insert_spoof_data(conn)
    conn.close()
    print("Database created and ~50 rows of spoof data inserted successfully.")


if __name__ == "__main__":
    main()
