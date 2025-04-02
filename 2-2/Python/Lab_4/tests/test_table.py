import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.column import Column
from Lab_4.minidb.datatypes import IntegerType, StringType
from Lab_4.minidb.table import Table

class TestTable(unittest.TestCase):
    def setUp(self):
        self.columns = [
            Column("id", IntegerType(0)),
            Column("name", StringType(""), nullable=False)
        ]
        self.table = Table("test", self.columns)

    def test_insert_row(self):
        self.table.insert({"id": 1, "name": "Bob"})
        self.assertEqual(len(self.table), 1)

    def test_get_rows(self):
        self.table.insert({"id": 2, "name": "Alice"})
        row = self.table.get_rows(0)
        self.assertEqual(row["name"], "Alice")

    def test_update_row(self):
        self.table.insert({"id": 3, "name": "Charlie"})
        row_id = self.table.get_rows(0).id
        self.table.update(row_id, {"name": "Dave"})
        updated_row = self.table.get_row_by_id(row_id)
        self.assertEqual(updated_row["name"], "Dave")

    def test_delete_row(self):
        self.table.insert({"id": 4, "name": "Eve"})
        row_id = self.table.get_rows(0).id
        self.table.delete(row_id)
        self.assertEqual(len(self.table), 0)
    
    def test_table_insert_missing_column(self):
        cols = [
            Column("id", IntegerType(0)),
            Column("name", StringType(""), nullable=False)
        ]
        table = Table("missing_col_test", cols)
        with self.assertRaises(ValueError):
            table.insert({"id": 123})    