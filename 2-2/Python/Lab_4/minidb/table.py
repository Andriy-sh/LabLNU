from .row import Row

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = {column.name: column for column in columns}
        self.rows = []
    
    def insert(self, row_data):
        row = Row(self.columns.values())
        for column_name, column in self.columns.items():
            value = row_data.get(column_name)
            row[column_name] = value
        self.rows.append(row)
            
    def get_rows(self, index):
        return self.rows[index]
    
    def get_row_by_id(self, row_id):
        for row in self.rows:
            if row.id == row_id:
                return row
        return None    
    
    def update(self, row_id, row_data):
        row = self.get_row_by_id(row_id)
        if row is None:
            raise ValueError(f'Row with ID {row_id} does not exist')
        for key, value in row_data.items():
            row[key] = value
    
    def delete(self, row_id):
        row = self.get_row_by_id(row_id)
        if row is None:
            raise ValueError(f'Row with ID {row_id} does not exist')
        self.rows.remove(row)
        
    def __len__(self):
        return len(self.rows)
    
    def __iter__(self):
        return iter(self.rows)