from .row import Row


class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = {column.name: column for column in columns}
        self.rows = []
        self.next_id = 1

    def insert(self, row_data):
        for column_name, column in self.columns.items():
            value = row_data.get(column_name)
            if not column.validate(value):
                raise ValueError(f"Invalid value for column {column_name}: {value}")
        row = Row(row_data)
        row.id = self.next_id
        self.next_id += 1
        self.rows.append(row)
        return row

    def get_by_id(self, id):
        for row in self.rows:
            if row.id == id:
                return row
        return None

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)
