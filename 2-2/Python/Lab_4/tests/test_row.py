import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.row import Row
from Lab_4.minidb.column import Column
from Lab_4.minidb.datatypes import IntegerType

class TestRow(unittest.TestCase):
    def setUp(self):
        Row._id_counter = 1
    def test_row_creation_and_id(self):
        columns = [Column("id", IntegerType(0))]
        row = Row(columns)
        self.assertEqual(row.id, 1)
        row2 = Row(columns)
        self.assertEqual(row2.id, 2)

    def test_row_set_and_get_item(self):
        columns = [Column("age", IntegerType(0))]
        row = Row(columns)
        row["age"] = 35
        self.assertEqual(row["age"], 35)

    def test_row_set_non_existent(self):
        columns = [Column("age", IntegerType(0))]
        row = Row(columns)
        with self.assertRaises(ValueError):
            row["name"] = "Alice"