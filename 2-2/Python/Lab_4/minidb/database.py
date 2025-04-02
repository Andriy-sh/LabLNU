import datetime
import json
from contextlib import contextmanager
import os
from .table import Table
from .column import Column
from .datatypes import IntegerType, StringType, BooleanType, DateType

class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}
    
    def create_table(self, name, columns):
        self.tables[name] = Table(name, columns)
    
    def delete_table(self, name):
        del self.tables[name]
    
    @contextmanager
    def write(self, filename):
        tmp_filename = filename + '.tmp'
        f = open(tmp_filename, 'w', encoding='utf-8')
        try:
            yield f
            f.close()
            os.replace(tmp_filename, filename)  
        except:
            f.close()
            if os.path.exists(tmp_filename):
                os.remove(tmp_filename)
            raise
    def save(self, filename):
        data = {
            'name': self.name,
            'tables': {}
        }
        for table_name, table in self.tables.items():
            data['tables'][table_name] = {
                'columns': [
                    (col_name, col.data_type.__class__.__name__, col.nullable)
                    for col_name, col in table.columns.items()
                ],
                'rows': [row.data for row in table.rows]
            }
        with self.write(filename) as f:
            json.dump(data, f, indent=4)
    
    def load(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.name = data['name']
        self.tables = {}
        for table_name, table_info in data['tables'].items():
            cols = []
            for col_def in table_info['columns']:
                col_name, dtype_name, nullable = col_def
                if dtype_name == 'IntegerType':
                    cols.append(Column(col_name, IntegerType(0), nullable))
                elif dtype_name == 'StringType':
                    cols.append(Column(col_name, StringType(''), nullable))
                elif dtype_name == 'BooleanType':
                    cols.append(Column(col_name, BooleanType(False), nullable))
                elif dtype_name == 'DateType':
                    cols.append(Column(col_name, DateType(datetime.date(1970, 1, 1)), nullable))
            new_table = Table(table_name, cols)
            for row_dict in table_info['rows']:
                new_table.insert(row_dict)
            self.tables[table_name] = new_table