from Lab4.minidb.database import Database
from Lab4.minidb.datatypes import IntegerType, StringType, BooleanType

from Lab4.minidb.column import Column
from Lab4.minidb.query import SimpleQuery

db = Database("mydb")

users_table = db.create_table("users", [''
    Column("id", IntegerType(), nullable=False),
    Column("name", StringType(max_length=50), nullable=False),
    Column("age", IntegerType(), nullable=True),
    Column("active", BooleanType(), nullable=False)
])

row1 = users_table.insert({"id": 1, "name": "Анна", "age": 30, "active": True})
row2 = users_table.insert({"id": 2, "name": "Богдан", "age": 25, "active": False})
row3 = users_table.insert({"id": 3, "name": "Василь", "age": 35, "active": True})

print("Всі користувачі:")
for row in users_table:
    print(row)

user = users_table.get_by_id(row1.id)
print(f"\nКористувач з id={row1.id}: {user}")

results = (SimpleQuery(users_table)
           .select(["name", "age"])
           .where("active", "=", True)
           .order_by("age")
           .execute())

print("\nАктивні користувачі (ім'я та вік):")
for row in results:
    print(f"Ім'я: {row['name']}, Вік: {row['age']}")

db.save("mydb.json")

loaded_db = Database.load("mydb.json")
print("\nЗавантажена база даних:")
print(f"Назва бази даних: {loaded_db.name}")
print(f"Таблиці: {list(loaded_db.tables.keys())}")
