import unittest

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.column import Column
from Lab_4.minidb.datatypes import IntegerType, StringType

class TestColumn(unittest.TestCase):
    def setUp(self):
        self.col_int = Column("age", IntegerType(0))
        self.col_str = Column("name", StringType(""), nullable=True)

    def test_column_validate_type_valid(self):
        self.col_int.validate_type(25)  

    def test_column_validate_type_invalid(self):
        with self.assertRaises(ValueError):
            self.col_int.validate_type("not int")

    def test_column_string(self):
        self.assertIn("age", str(self.col_int))