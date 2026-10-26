import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        self.db_path = Path("data/tournament.db")

        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.connection = sqlite3.connect(
            self.db_path
        )

        self.connection.row_factory = sqlite3.Row

        self.initialize()

    def initialize(self):
        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
                    CHECK(role IN ('player', 'organizer'))
            )
            """
        )

        self.connection.commit()

        self.seed_users()

    def seed_users(self):
        users = [
            ("player", "player123", "player"),
            ("organizer", "organizer123", "organizer"),
        ]

        for username, password, role in users:
            self.connection.execute(
                """
                INSERT OR IGNORE INTO users
                (username, password, role)
                VALUES (?, ?, ?)
                """,
                (username, password, role),
            )

        self.connection.commit()

    def get_user_by_username(self, username):
        cursor = self.connection.execute(
            """
            SELECT username, password, role
            FROM users
            WHERE username = ?
            """,
            (username,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    def close(self):
        self.connection.close()