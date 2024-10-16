import mysql.connector
import csv


def connect_to_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lab5'
    )
    return connection


def show_tables(cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    return [table[0] for table in tables]


def execute_select_query(cursor, query):
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def save_to_csv(results, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(results)


def main():
    connection = connect_to_db()
    cursor = connection.cursor()

    while True:
        print("\nМеню:")
        print("1. Показати таблиці")
        print("2. Виконати SELECT-запит")
        print("3. Зберегти результати у CSV")
        print("4. Вийти")

        choice = input("Виберіть опцію (1-4): ")

        if choice == '1':
            tables = show_tables(cursor)
            print("Таблиці бази даних:")
            for table in tables:
                print(table)

        elif choice == '2':
            query = input("Введіть SELECT-запит: ")
            if query:
                results = execute_select_query(cursor, query)
                if results is not None:
                    print("Результати запиту:")
                    for row in results:
                        print(row)

        elif choice == '3':
            filename = input("Введіть назву файлу (з розширенням .csv): ")
            results = []
            query = input("Введіть SELECT-запит для експорту: ")
            if query:
                results = execute_select_query(cursor, query)
                if results is not None:
                    save_to_csv(results, filename)
                    print(f"Дані успішно збережено у {filename}")

        elif choice == '4':
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
