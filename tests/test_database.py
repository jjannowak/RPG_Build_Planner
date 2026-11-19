
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from contextlib import closing

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        """Create a temporary database for each test."""

        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "test_items.db"

        self.db_patcher = patch.object(
            database,
            "DB_PATH",
            self.db_path,
        )
        self.db_patcher.start()

        database.initialize_database()

    def tearDown(self):
        """Clean up the temporary database."""

        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def get_expected_items(self):
        json_path = Path(database.__file__).parent / "data" / "items.json"

        with open(json_path, encoding="utf-8") as file:
            return json.load(file)

    def test_database_creates_items_table(self):
        with closing(sqlite3.connect(self.db_path)) as connection:
            with connection:
                cursor = connection.execute(
                    "SELECT name FROM sqlite_master "
                    "WHERE type='table' AND name='items'"
                )

            result = cursor.fetchone()

        self.assertIsNotNone(result)

    def test_database_starts_empty(self):
        items = database.get_all_items()

        self.assertEqual(items, [])

    def test_import_items_from_json(self):
        database.import_items_from_json()

        items = database.get_all_items()
        expected_items = self.get_expected_items()

        self.assertEqual(len(items), len(expected_items))

        self.assertEqual(
            {item["id"] for item in items},
            {item["id"] for item in expected_items},
        )

    def test_import_does_not_create_duplicates(self):
        database.import_items_from_json()
        database.import_items_from_json()

        items = database.get_all_items()
        expected_items = self.get_expected_items()

        self.assertEqual(len(items), len(expected_items))

        ids = [item["id"] for item in items]

        self.assertEqual(len(ids), len(set(ids)))

    def test_imported_items_have_required_fields(self):
        database.import_items_from_json()

        items = database.get_all_items()

        required_fields = {
            "id",
            "name",
            "category",
            "weight",
            "strength_required",
            "dexterity_required",
            "damage",
            "scaling_attribute",
        }

        for item in items:
            with self.subTest(item=item["name"]):
                self.assertTrue(required_fields.issubset(item.keys()))


if __name__ == "__main__":
    unittest.main()
