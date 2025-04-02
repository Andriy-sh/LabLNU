import unittest
import datetime

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.datatypes import IntegerType, StringType, BooleanType, DateType
from Lab_4.minidb.table import Table
from Lab_4.minidb.column import Column

class TestDataType(unittest.TestCase):
    def test_integer_type_valid(self):
        obj = IntegerType(10)
        self.assertEqual(obj.value, 10)

    def test_integer_type_invalid(self):
        with self.assertRaises(ValueError):
            IntegerType("abc")

    def test_string_type_valid(self):
        obj = StringType("hello")
        self.assertEqual(obj.value, "hello")

    def test_string_type_invalid(self):
        with self.assertRaises(ValueError):
            StringType(123)

    def test_date_type_valid(self):
        d = datetime.date(2025, 3, 10)
        obj = DateType(d)
        self.assertEqual(obj.value, d)

    def test_date_type_invalid(self):
        with self.assertRaises(ValueError):
            DateType("not a date")

    def test_boolean_type_valid(self):
        obj = BooleanType(True)
        self.assertTrue(obj.value)

    def test_boolean_type_invalid(self):
        with self.assertRaises(ValueError):
            BooleanType("true")
    
    def test_date_type_string(self):
        with self.assertRaises(ValueError):
            DateType("2025-03-10") 

    def test_boolean_type_int(self):

        with self.assertRaises(ValueError):
            BooleanType(1)        
            
    def test_table_insert_invalid_data_type(self):
        table = Table("invalid_test", [Column("value", IntegerType(0))])
        with self.assertRaises(ValueError):
            table.insert({"value": "text, not int"})
            