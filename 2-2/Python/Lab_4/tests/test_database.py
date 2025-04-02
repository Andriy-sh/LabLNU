import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.database import Database
from Lab_4.minidb.column import Column
from Lab_4.minidb.datatypes import StringType

class TestDatabase(unittest.TestCase):
    def test_database_create_and_delete(self):
        db = Database("MyDB")
        db.create_table("people", [Column("name", StringType(""))])
        self.assertIn("people", db.tables)
        db.delete_table("people")
        self.assertNotIn("people", db.tables)

    def test_database_save_and_load(self):
        db = Database("MyDB")
        db.create_table("people", [Column("name", StringType(""))])
        db.tables["people"].insert({"name": "Marry"})
        db.save("test_db.json")

        db2 = Database("Empty")
        db2.load("test_db.json")
        self.assertEqual(db2.name, "MyDB")
        self.assertIn("people", db2.tables)
        self.assertEqual(len(db2.tables["people"]), 1)