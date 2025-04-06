import sqlite3


class SQLiteDB:
    def __init__(self, name):
        self.name = f"{name}.db"
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, fields):
        columns = ", ".join([f"{key} {value}" for key, value in fields.items()])
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})")
        self.conn.commit()

    def create(self, table_name, data):
        columns = ", ".join(data.keys())
        placeholders = ", ".join(['?' for _ in data])
        values = tuple(data.values())
        self.cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()
        return self.get(table_name, self.cursor.lastrowid)

    def get(self, table_name, obj_id):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE id = ?", (obj_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [col[0] for col in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def update(self, table_name, obj_id, data):
        updates = ", ".join([f"{key} = ?" for key in data])
        values = tuple(data.values()) + (obj_id,)
        self.cursor.execute(f"UPDATE {table_name} SET {updates} WHERE id = ?", values)
        self.conn.commit()
        return self.get(table_name, obj_id)

    def delete(self, table_name, obj_id):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (obj_id,))
        self.conn.commit()
        return True
