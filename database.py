
import json
import sqlite3
from pathlib import Path
from contextlib import closing


DB_PATH = Path(__file__).parent / "data" / "items.db"
JSON_PATH = Path(__file__).parent / "data" / "items.json"


def initialize_database():
    """Create the database and items table if they do not exist."""

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    category TEXT NOT NULL,
                    weight REAL NOT NULL,
                    strength_required INTEGER NOT NULL,
                    dexterity_required INTEGER NOT NULL,
                    damage INTEGER NOT NULL,
                    scaling_attribute TEXT NOT NULL
                )
            """)


def import_items_from_json():
    """Import items from JSON into the SQLite database."""

    with open(JSON_PATH, "r", encoding="utf-8") as file:
        items = json.load(file)

    with closing(sqlite3.connect(DB_PATH)) as connection:
        with connection:
            connection.executemany("""
                INSERT INTO items (
                    id,
                    name,
                    category,
                    weight,
                    strength_required,
                    dexterity_required,
                    damage,
                    scaling_attribute
                )
                VALUES (
                    :id,
                    :name,
                    :category,
                    :weight,
                    :strength_required,
                    :dexterity_required,
                    :damage,
                    :scaling_attribute
                )
                ON CONFLICT(id) DO UPDATE SET
                    name = excluded.name,
                    category = excluded.category,
                    weight = excluded.weight,
                    strength_required = excluded.strength_required,
                    dexterity_required = excluded.dexterity_required,
                    damage = excluded.damage,
                    scaling_attribute = excluded.scaling_attribute
            """, items)


def get_all_items():
    """Retrieve all items from the SQLite database."""

    with closing(sqlite3.connect(DB_PATH)) as connection:
        connection.row_factory = sqlite3.Row

        cursor = connection.execute(
            "SELECT * FROM items ORDER BY id"
        )

        return [dict(row) for row in cursor.fetchall()]
