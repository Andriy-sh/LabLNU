import mysql.connector


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
    print("Таблиці бази даних:")
    for table in tables:
        print(table[0])


def show_table_structure(cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"\nСтруктура таблиці: {table[0]}")
        cursor.execute(f"DESCRIBE {table[0]}")
        structure = cursor.fetchall()
        for column in structure:
            print(column)


def math_ps(cursor):
    cursor.execute("""
        SELECT 
            case_type AS `Тип справи`,
            article_code AS `Код статті`,
            punishment_max AS `Максимальний термін`, 
            punishment_min AS `Мінімальний термін`, 
            (punishment_max + punishment_min) / 2 AS `Середній термін` 
        FROM cases;
    """)
    result = cursor.fetchall()

    print("\nЗапит з псевдонімами та математичними операціями:")
    print(
        f"{'Тип справи':<25} {'Код статті':<15} {'Максимальний термін':<20} {'Мінімальний термін':<20} {'Середній термін':<20}")
    print("=" * 100)

    for row in result:
        print(f"{row[0]:<25} || {row[1]:<15} || {row[2]:<20} || {row[3]:<20} || {row[4]:<20}")


def filter(cursor):
    cursor.execute("SELECT * FROM cases WHERE punishment_min > 4 AND punishment_max < 11;")
    result = cursor.fetchall()
    print("\nЗапит з фільтрацією по стовпцю:")
    for row in result:
        print(row)


def sorting(cursor):
    cursor.execute(
        "SELECT case_type AS `Тип справи`, article_code AS `Код статті`, punishment_max AS `Максимальний термін`, punishment_min AS `Мінімальний термін`, fee AS `Вартість` FROM cases ORDER BY fee DESC;")
    result = cursor.fetchall()

    print("\nЗапит з сортуванням результатів:")
    print(
        f"{'Тип справи':<30} {'Код статті':<23} {'Максимальний термін':<28} {'Мінімальний термін':<28} {'Вартість':<15}")
    print("=" * 200)

    for row in result:
        print(f"{row[0]:<30} || {row[1]:<20} || {row[2]:<25} || {row[3]:<25} || {row[4]:<15}")


def insert_data(cursor, connection):
    cursor.execute("""
        INSERT INTO clients (full_name, birth_date, address, phone, status) 
        VALUES ('Новий Клієнт', '1991-01-01', 'м. Київ, вул. Нова, 1', '+380631111111', 'фізична особа');
    """)
    connection.commit()
    print("\nНовий запис додано до таблиці clients.")


def update_data(cursor, connection):
    cursor.execute("""
        UPDATE cases SET case_status = 'завершена' WHERE case_id = 2;
    """)
    connection.commit()
    print("\nДані оновлено.")


def logical_operators(cursor):
    cursor.execute("""
        SELECT 
            case_type AS `Тип справи`, 
            article_code AS `Код статті`,
            punishment_max AS `Максимальний термін`, 
            punishment_min AS `Мінімальний термін`, 
            case_status AS `Статус справи`
        FROM cases 
        WHERE 
            punishment_min > 5 
            AND punishment_max < 15 
            OR case_status NOT LIKE 'активна';
    """)

    result = cursor.fetchall()

    print("\nЗапит з використанням операторів AND, OR, NOT:")
    print(
        f"{'Тип справи':<30} {'Код статті':<23} {'Максимальний термін':<23} {'Мінімальний термін':<23} {'Статус справи':<20}")
    print("=" * 110)

    for row in result:
        print(f"{row[0]:<30} || {row[1]:<20} || {row[2]:<20} || {row[3]:<20} || {row[4]:<20}")


# Основна функція
def main():
    connection = connect_to_db()
    cursor = connection.cursor()

    show_tables(cursor)
    show_table_structure(cursor)
    math_ps(cursor)
    filter(cursor)
    logical_operators(cursor)
    sorting(cursor)
    insert_data(cursor, connection)
    update_data(cursor, connection)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
