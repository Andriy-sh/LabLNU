import json
from datetime import datetime
import random
def load_data():
    """
    Завантажує дані з файлу data.json. Якщо файл не знайдено, повертає базову структуру даних.

    Returns:
        dict: Словник з даними про столики, меню, замовлення та звіти.
    """
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "tables": [],
            "menu": [],
            "orders": [],
            "reports": []
        }

def save_data(data):
    """
    Зберігає дані у файл data.json.

    Args:
        data (dict): Словник з даними для збереження.
    """
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)

def initialize_tables():
    """
    Ініціалізує столики, якщо вони ще не ініціалізовані.
    Створює 15 столиків з місткістю від 1 до 8 місць.
    """
    data = load_data()
    if not data["tables"]:
        data["tables"] = [{"id": i+1, "capacity": i+2, "status": "free", "reserved_time": None} for i in range(15)]
        save_data(data)

def initialize_menu():
    """
    Ініціалізує меню, якщо воно ще не ініціалізоване.
    Додає базові страви до меню.
    """
    data = load_data()
    if not data["menu"]:
        data["menu"] = [
            {"id": 1, "name": "Курячий суп", "category": "основна страва", "price": 60, "prep_time": 20, "modifications": []},
            {"id": 2, "name": "Вегетаріанська паста", "category": "основна страва", "price": 140, "prep_time": 25, "modifications": ["без часнику"]},
            {"id": 3, "name": "Лосось на грилі", "category": "основна страва", "price": 220, "prep_time": 30, "modifications": []},
            {"id": 4, "name": "Безалкогольний напій", "category": "напій", "price": 30, "prep_time": 5, "modifications": []},
        ]
        save_data(data)

def view_tables():
    """
    Виводить інформацію про всі столики, включаючи їх статус, місткість та час бронювання.
    """
    data = load_data()
    for table in data["tables"]:
        print(f"Столик {table['id']}: {table['status']}, Місткість: {table['capacity']}, Час бронювання: {table['reserved_time']}")

def reserve_table(table_id, time):
    """
    Бронює столик на вказаний час, якщо він доступний.

    Args:
        table_id (int): Номер столика.
        time (str): Час бронювання у форматі "гг:хх".
    """
    data = load_data()
    for table in data["tables"]:
        if table["id"] == table_id and table["status"] == "free":
            table["status"] = "reserved"
            table["reserved_time"] = time
            save_data(data)
            print(f"Столик {table_id} заброньовано на {time}.")
            return
    print("Столик недоступний для бронювання.")

def free_table(table_id):
    """
    Звільняє столик, якщо він був зайнятий або заброньований.

    Args:
        table_id (int): Номер столика.
    """
    data = load_data()
    for table in data["tables"]:
        if table["id"] == table_id:
            table["status"] = "free"
            table["reserved_time"] = None
            save_data(data)
            print(f"Столик {table_id} звільнено.")
            return
    print("Столик не знайдено.")

def add_order(table_id, items, special_requests=None):
    data = load_data()
    
    for table in data["tables"]:
        if table["id"] == table_id:
            if table["status"] == "free" or table["status"] == "reserved":
                table["status"] = "occupied"
                table["reserved_time"] = None
            else:
                print(f"Столик {table_id} вже зайнятий.")
                return
    
    order = {
        "id": len(data["orders"]) + 1,
        "table_id": table_id,
        "items": items,
        "special_requests": special_requests, 
        "status": "прийнято",
        "total_price": sum(item["price"] for item in items),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["orders"].append(order)
    save_data(data)
    print(f"Замовлення {order['id']} додано. Столик {table_id} тепер зайнятий.")


def calculate_bill(order_id, discounts=None):
    data = load_data()
    order = next((order for order in data["orders"] if order["id"] == order_id), None)
    if order:
        total = order["total_price"]
        discount_applied = None
        if discounts:
            for discount in discounts:
                if discount == "1":
                    discount_applied = "Студентська знижка (10%)"
                    total *= 0.9
                elif discount == "2":
                    discount_applied = "Пенсійна знижка (15%)"
                    total *= 0.85
                elif discount == "3":
                    discount_applied = "Години знижок (20%)"
                    total *= 0.8

        tax = total * 0.08
        tip = total * random.uniform(0, 0.10)
        total += tax + tip

        if discount_applied:
            print(f"Застосована знижка: {discount_applied}")
        else:
            print("Знижка не застосовувалася.")

        print(f"Рахунок для замовлення {order_id}: {total:.2f} грн (податок: {tax:.2f} грн, чайові: {tip:.2f} грн)")
    else:
        print("Замовлення не знайдено.")

def generate_report():
    """
    Генерує звіт про загальний обсяг продажів та найпопулярнішу страву.
    """
    data = load_data()
    total_sales = sum(order["total_price"] for order in data["orders"])
    popular_items = {}
    for order in data["orders"]:
        for item in order["items"]:
            popular_items[item["name"]] = popular_items.get(item["name"], 0) + 1
    most_popular = max(popular_items, key=popular_items.get)
    print(f"Загальний обсяг продажів: {total_sales} грн")
    print(f"Найпопулярніша страва: {most_popular}")
def info(table_id):
    """
    Виводить інформацію про конкретний столик за його ID, включаючи замовлені страви.

    Args:
        table_id (int): Номер столика.
    """
    data = load_data()
    table = next((table for table in data["tables"] if table["id"] == table_id), None)
    if table:
        print(f"Інформація про столик {table_id}:")
        print(f"Статус: {table['status']}")
        print(f"Місткість: {table['capacity']}")
        print(f"Час бронювання: {table['reserved_time']}")

        orders_for_table = [order for order in data["orders"] if order["table_id"] == table_id]
        if orders_for_table:
            print("\nЗамовлення для цього столика:")
            for order in orders_for_table:
                print(f"Замовлення #{order['id']}:")
                for item in order["items"]:
                    print(f"  - {item['name']} ({item['price']} грн)")
                print(f"  Загальна сума: {order['total_price']} грн")
        else:
            print("Для цього столика немає замовлень.")
    else:
        print(f"Столик {table_id} не знайдено.")
def main():
    """
    Головний цикл програми, який забезпечує взаємодію з користувачем через консоль.
    """
    initialize_tables()
    initialize_menu()
    while True:
        print("\n1. Перегляд столиків\n2. Додати замовлення\n3. Звільнення столика\n4. Розрахувати рахунок\n5. Звіт\n6. Інформація про столик\n7. Вийти")
        choice = input("Оберіть опцію: ")
        if choice == "1":
            view_tables()
        elif choice == "2":
            print("\nДоступні страви:")
            data = load_data()
            for item in data["menu"]:
                print(f"{item['id']}. {item['name']} ({item['category']}) - {item['price']} грн")

            table_id = int(input("Введіть номер столика: "))
            items = []
            while True:
                item_id = input("Введіть ID страви (або 'готово' для завершення): ")
                if item_id == "готово":
                    break
                try:
                    item_id = int(item_id)
                    item = next((item for item in data["menu"] if item["id"] == item_id), None)
                    if item:
                        items.append(item)
                        print(f"Додано: {item['name']}")
                    else:
                        print("Невірний ID страви. Спробуйте ще раз.")
                except ValueError:
                    print("Будь ласка, введіть числовий ID.")
            add_order(table_id, items)
        elif choice == "3":
            table_id = int(input("Введіть номер столика: "))
            free_table(table_id)
        elif choice == "4":
            order_id = int(input("Введіть номер замовлення: "))
            discounts = input("Введіть знижки (1.Студентська, 2.Пенсійна, 3.Години знижок): ").split(",")
            calculate_bill(order_id, discounts)
        elif choice == "5":
            generate_report()
        elif choice == "6":
            table_id = int(input("Введіть номер столика: "))
            info(table_id)
        elif choice == "7":
            break
        else:
            print("Невірний вибір. Спробуйте ще раз.")
if __name__ == "__main__":
    main()