import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.column import Column
from Lab_4.minidb.table import Table
from Lab_4.minidb.datatypes import IntegerType, StringType
from Lab_4.minidb.query import SimpleQuery, JoinedTable

class TestSimpleQuery(unittest.TestCase):
    def setUp(self):
        cols = [Column("qty", IntegerType(0))]
        self.table = Table("test_query", cols)
        self.table.insert({"qty": 5})
        self.table.insert({"qty": 10})
        self.table.insert({"qty": 15})

    def test_count(self):
        q = SimpleQuery(self.table)
        self.assertEqual(q.aggregate_count(), 3)

    def test_sum(self):
        q = SimpleQuery(self.table).aggregate("qty")
        self.assertEqual(q.aggregate_sum(), 30)

    def test_avg(self):
        q = SimpleQuery(self.table).aggregate("qty")
        self.assertEqual(q.aggregate_avg(), 10)

class TestJoinedTable(unittest.TestCase):
    def test_joined_table(self):
        t1 = Table("t1", [Column("id", IntegerType(0))])
        t2 = Table("t2", [Column("uid", IntegerType(0)), Column("val", StringType(""))])
        t1.insert({"id": 1})
        t1.insert({"id": 2})
        t2.insert({"uid": 2, "val": "Data"})

        joined = JoinedTable(t1, t2, "id", "uid")
        result = list(joined)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 2)
        self.assertEqual(result[0]["val"], "Data")