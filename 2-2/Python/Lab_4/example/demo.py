import sys
import os

from Lab_4.minidb.database import Database

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Lab_4.minidb.datatypes import IntegerType, StringType, BooleanType
from Lab_4.minidb.column import Column
from Lab_4.minidb.query import SimpleQuery, JoinedTable

db = Database("TestDB")

users_columns = [
    Column("id", IntegerType(0)),
    Column("name", StringType("")),
    Column("active", BooleanType(True))
]
db.create_table("users", users_columns)

users_table = db.tables["users"]
users_table.insert({"id": 1, "name": "Alice", "active": True})
users_table.insert({"id": 2, "name": "Bob", "active": False})
users_table.insert({"id": 3, "name": "Charlie", "active": True})

print("\nВсі користувачі:")
for row in users_table:
    print(row)

print("\nАктивні користувачі:")
query = SimpleQuery(users_table).where(("active", "=", True))
for row in query.execute():
    print(row)

orders_columns = [
    Column("order_id", IntegerType(0)),
    Column("user_id", IntegerType(0)),
    Column("amount", IntegerType(0))
]
db.create_table("orders", orders_columns)

orders_table = db.tables["orders"]
orders_table.insert({"order_id": 101, "user_id": 1, "amount": 250})
orders_table.insert({"order_id": 102, "user_id": 3, "amount": 100})

print("\nВсі замовлення:")
for row in orders_table:
    print(row)

print("\nОб'єднані таблиці (користувачі та їхні замовлення):")
joined = JoinedTable(users_table, orders_table, "id", "user_id")
for row in joined:
    print(row)

query = SimpleQuery(orders_table).aggregate("amount")
print("\nЗагальна сума замовлень:", query.aggregate_sum())

db.save("database.json")
print("\nБаза даних збережена у 'database.json'.")

db2 = Database("LoadedDB")
db2.load("database.json")
print("\nБаза даних успішно завантажена. Назва:", db2.name)
