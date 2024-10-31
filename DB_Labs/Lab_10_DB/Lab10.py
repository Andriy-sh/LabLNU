import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox

class Lawyer:
    def __init__(self, name, birth_date, address, phone, education, position, experience_years, lawyer_id=None):
        self.id = lawyer_id
        self.name = name
        self.birth_date = birth_date
        self.address = address
        self.phone = phone
        self.education = education
        self.position = position
        self.experience_years = experience_years

class ILawyerDAO:
    def add_lawyer(self, lawyer):
        pass

    def find_by_id(self, lawyer_id):
        pass

    def find_by_name(self, name):
        pass

    def update_lawyer(self, lawyer):
        pass

    def delete_lawyer(self, lawyer_id):
        pass

class LawyerDAOMySQL(ILawyerDAO):
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )

    def add_lawyer(self, lawyer):
        cursor = self.connection.cursor()
        query = """INSERT INTO lawyers (name, birth_date, address, phone, education, position, experience_years)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (lawyer.name, lawyer.birth_date, lawyer.address, lawyer.phone,
                               lawyer.education, lawyer.position, lawyer.experience_years))
        self.connection.commit()

    def find_by_id(self, lawyer_id):
        cursor = self.connection.cursor()
        query = "SELECT * FROM lawyers WHERE id = %s"
        cursor.execute(query, (lawyer_id,))
        result = cursor.fetchone()
        if result:
            return Lawyer(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[0])
        return None

    def update_lawyer(self, lawyer):
        cursor = self.connection.cursor()
        query = """UPDATE lawyers SET name = %s, birth_date = %s, address = %s, phone = %s, 
                   education = %s, position = %s, experience_years = %s WHERE id = %s"""
        cursor.execute(query, (lawyer.name, lawyer.birth_date, lawyer.address, lawyer.phone, lawyer.education,
                               lawyer.position, lawyer.experience_years, lawyer.id))
        self.connection.commit()

    def delete_lawyer(self, lawyer_id):
        cursor = self.connection.cursor()
        lawyer = self.find_by_id(lawyer_id)
        if lawyer:
            query = "DELETE FROM lawyers WHERE id = %s"
            cursor.execute(query, (lawyer_id,))
            self.connection.commit()
        else:
            print(f"Юриста з ID {lawyer_id} не знайдено.")

class LawyerGUI:
    def __init__(self, root, dao):
        self.dao = dao
        self.root = root
        self.root.title("Управління юристами")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Ім'я").grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Дата народження").grid(row=1, column=0)
        self.birth_date_entry = tk.Entry(self.root)
        self.birth_date_entry.grid(row=1, column=1)

        tk.Label(self.root, text="Адреса").grid(row=2, column=0)
        self.address_entry = tk.Entry(self.root)
        self.address_entry.grid(row=2, column=1)

        tk.Label(self.root, text="Телефон").grid(row=3, column=0)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Освіта").grid(row=4, column=0)
        self.education_entry = tk.Entry(self.root)
        self.education_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Посада").grid(row=5, column=0)
        self.position_entry = tk.Entry(self.root)
        self.position_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Досвід (років)").grid(row=6, column=0)
        self.experience_entry = tk.Entry(self.root)
        self.experience_entry.grid(row=6, column=1)

        self.add_button = tk.Button(self.root, text="Додати юриста", command=self.add_lawyer)
        self.add_button.grid(row=7, column=0, columnspan=2)

        self.update_button = tk.Button(self.root, text="Оновити юриста", command=self.update_lawyer)
        self.update_button.grid(row=8, column=0, columnspan=2)

        self.delete_button = tk.Button(self.root, text="Видалити юриста", command=self.delete_lawyer)
        self.delete_button.grid(row=9, column=0, columnspan=2)

        tk.Label(self.root, text="ID для пошуку/видалення").grid(row=10, column=0)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.grid(row=10, column=1)

        self.find_button = tk.Button(self.root, text="Знайти юриста", command=self.find_lawyer)
        self.find_button.grid(row=11, column=0, columnspan=2)

    def add_lawyer(self):
        lawyer = Lawyer(
            name=self.name_entry.get(),
            birth_date=self.birth_date_entry.get(),
            address=self.address_entry.get(),
            phone=self.phone_entry.get(),
            education=self.education_entry.get(),
            position=self.position_entry.get(),
            experience_years=int(self.experience_entry.get())
        )
        try:
            self.dao.add_lawyer(lawyer)
            messagebox.showinfo("Успіх", "Юриста додано успішно!")
        except Error as e:
            messagebox.showerror("Помилка", f"Не вдалося додати юриста: {e}")

    def find_lawyer(self):
        lawyer_id = self.id_entry.get()
        try:
            lawyer = self.dao.find_by_id(lawyer_id)
            if lawyer:
                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, lawyer.name)

                self.birth_date_entry.delete(0, tk.END)
                self.birth_date_entry.insert(0, lawyer.birth_date)

                self.address_entry.delete(0, tk.END)
                self.address_entry.insert(0, lawyer.address)

                self.phone_entry.delete(0, tk.END)
                self.phone_entry.insert(0, lawyer.phone)

                self.education_entry.delete(0, tk.END)
                self.education_entry.insert(0, lawyer.education)

                self.position_entry.delete(0, tk.END)
                self.position_entry.insert(0, lawyer.position)

                self.experience_entry.delete(0, tk.END)
                self.experience_entry.insert(0, str(lawyer.experience_years))

            else:
                messagebox.showwarning("Помилка", "Юриста не знайдено")
        except Error as e:
            messagebox.showerror("Помилка", f"Не вдалося знайти юриста: {e}")

    def update_lawyer(self):
        lawyer_id = self.id_entry.get()
        try:
            lawyer = self.dao.find_by_id(lawyer_id)
            if lawyer:
                lawyer.name = self.name_entry.get()
                lawyer.birth_date = self.birth_date_entry.get()
                lawyer.phone = self.phone_entry.get()
                lawyer.address = self.address_entry.get()
                lawyer.education = self.education_entry.get()
                lawyer.position = self.position_entry.get()
                lawyer.experience_years = int(self.experience_entry.get())

                self.dao.update_lawyer(lawyer)
                messagebox.showinfo("Успіх", "Інформацію про юриста оновлено")
            else:
                messagebox.showwarning("Помилка", "Юриста не знайдено")
        except Error as e:
            messagebox.showerror("Помилка", f"Не вдалося оновити юриста: {e}")

    def delete_lawyer(self):
        lawyer_id = self.id_entry.get()
        try:
            self.dao.delete_lawyer(lawyer_id)
            messagebox.showinfo("Успіх", "Юриста видалено")
        except Error as e:
            messagebox.showerror("Помилка", f"Не вдалося видалити юриста: {e}")

def main():
    dao = LawyerDAOMySQL(host="localhost", user="root", password="", database="lab5")
    root = tk.Tk()
    gui = LawyerGUI(root, dao)
    root.mainloop()

if __name__ == "__main__":
    main()
