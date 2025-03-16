from .table import Table  # Додано імпорт класу Table
import json

class Database:
    def __init__(self, name):
        self.name = name
        self.tables = {}

    def create_table(self, name, columns):
        table = Table(name, columns)  # Створення таблиці
        self.tables[name] = table
        return table

    def save(self, filename):
        data = {
            "name": self.name,
            "tables": {
                table_name: {
                    "columns": [str(col) for col in table.columns.values()],
                    "rows": [row.data for row in table.rows]
                }
                for table_name, table in self.tables.items()
            }
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        db = cls(data["name"])
        # Логіка завантаження таблиць та рядків...
        return db