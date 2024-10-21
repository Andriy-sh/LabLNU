import mysql.connector
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog


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


def on_show_tables():
    tables = show_tables(cursor)
    tables_listbox.delete(0, tk.END)
    for table in tables:
        tables_listbox.insert(tk.END, table)


def on_execute_query():
    query = query_entry.get()
    if query:
        try:
            results = execute_select_query(cursor, query)
            result_text.delete(1.0, tk.END)
            for row in results:
                result_text.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося виконати запит: {e}")
    else:
        messagebox.showwarning("Попередження", "Введіть SELECT-запит.")


def on_save_to_csv():
    query = query_entry.get()
    if query:
        try:
            results = execute_select_query(cursor, query)
            if results:
                filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if filename:
                    save_to_csv(results, filename)
                    messagebox.showinfo("Успіх", f"Дані успішно збережено у {filename}")
            else:
                messagebox.showwarning("Попередження", "Запит не повернув результатів.")
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося зберегти дані: {e}")
    else:
        messagebox.showwarning("Попередження", "Введіть SELECT-запит.")


def on_exit():
    cursor.close()
    connection.close()
    root.quit()


connection = connect_to_db()
cursor = connection.cursor()

root = tk.Tk()

root.geometry("900x600")
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=6)
style.configure("TEntry", font=("Helvetica", 12), padding=6)
style.configure("TLabel", font=("Helvetica", 12))
style.configure("TListbox", font=("Helvetica", 12))

frame = tk.Frame(root)
frame.pack(pady=20)

show_tables_button = ttk.Button(frame, text="Показати таблиці", command=on_show_tables)
show_tables_button.grid(row=0, column=0, padx=5, pady=10)

execute_query_button = ttk.Button(frame, text="Виконати SELECT-запит", command=on_execute_query)
execute_query_button.grid(row=0, column=1, padx=5, pady=10)

save_to_csv_button = ttk.Button(frame, text="Зберегти у CSV", command=on_save_to_csv)
save_to_csv_button.grid(row=0, column=2, padx=5, pady=10)

exit_button = ttk.Button(frame, text="Вийти", command=on_exit)
exit_button.grid(row=0, column=3, padx=5, pady=10)

tables_label = ttk.Label(root, text="Таблиці бази даних:")
tables_label.pack(pady=5)

tables_listbox = tk.Listbox(root, height=10, width=80, font=("Helvetica", 12))
tables_listbox.pack(pady=10)

query_label = ttk.Label(root, text="Введіть SELECT-запит:")
query_label.pack(pady=5)

query_entry = ttk.Entry(root, width=80)
query_entry.pack(pady=5)

result_label = ttk.Label(root, text="Результати запиту:")
result_label.pack(pady=5)

result_text = tk.Text(root, height=20, width=100, font=("Helvetica", 12), wrap="none")
result_text.pack(pady=10)

root.mainloop()
