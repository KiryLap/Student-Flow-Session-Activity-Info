import tkinter as tk
import customtkinter as ctk
import sqlite3

# Список предметов, групп и оценок
subjects = ["Math", "Science", "History", "English"]
groups = ["AA-23-07", "AA-23-08", "AC-23-04", "AC-23-05"]
grades = [str(grade) for grade in range(2, 6)]  # Список оценок от 2 до 5 в виде строк

# Создание базы данных и таблицы
def create_db():
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            lastname TEXT NOT NULL,  -- Добавлен новый столбец для фамилии
            subject TEXT NOT NULL,
            group_name TEXT NOT NULL,
            grade REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Добавление записи
def add_student():
    name = name_entry.get()
    lastname = lastname_entry.get()  # Получаем фамилию
    subject = subject_option_menu.get()
    group = group_option_menu.get()
    grade = grade_option_menu.get()

    if name and lastname and subject and group and grade:  # Проверяем нужные поля
        conn = sqlite3.connect('student_performance.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO students (name, lastname, subject, group_name, grade) VALUES (?, ?, ?, ?, ?)',
                       (name, lastname, subject, group, float(grade)))
        conn.commit()
        conn.close()
        update_student_list()

# Удаление записи по ID
def delete_student():
    student_id = delete_id_entry.get()

    if student_id:
        conn = sqlite3.connect('student_performance.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        update_student_list()
        delete_id_entry.delete(0, tk.END)

# Получение всех записей с фильтрацией по предмету и группе
def get_students(subject_filter=None, group_filter=None, order_by=None):
    conn = sqlite3.connect('student_performance.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM students'
    params = []

    if subject_filter and subject_filter != "All":
        query += ' WHERE subject = ?'
        params.append(subject_filter)

    if group_filter and group_filter != "All":
        if 'WHERE' in query:
            query += ' AND group_name = ?'
        else:
            query += ' WHERE group_name = ?'
        params.append(group_filter)

    if order_by:
        query += f' ORDER BY {order_by}'

    cursor.execute(query, params)
    records = cursor.fetchall()
    conn.close()
    return records

# Обновление списка студентов
def update_student_list(order_by=None):
    for widget in student_list_frame.winfo_children():
        widget.destroy()

    headers = ["ID", "Name", "Last Name", "Subject", "Group", "Grade"]  # Добавлено "Last Name"
    for idx, header in enumerate(headers):
        ctk.CTkLabel(student_list_frame, text=header, font=("Arial", 14)).grid(row=0, column=idx, padx=10, pady=5, sticky='nsew')

    subject_filter = subject_option_menu.get()
    group_filter = group_option_menu.get()
    students = get_students(subject_filter, group_filter, order_by)
    for idx, student in enumerate(students):
        for jdx, value in enumerate(student):
            ctk.CTkLabel(student_list_frame, text=value).grid(row=idx + 1, column=jdx, padx=10, pady=5, sticky='nsew')

    for i in range(len(headers)):
        student_list_frame.columnconfigure(i, weight=1)

# Сортировка по имени и фамилии
def sort_students(order_by):
    update_student_list(order_by)

# Основная функция
def main():
    create_db()  # Создание базы данных

    # Настройка интерфейса
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.title("Student Performance")

    # Первая колонка
    ctk.CTkLabel(app, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky='e')
    global name_entry
    name_entry = ctk.CTkEntry(app)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(app, text="Last Name").grid(row=1, column=0, padx=5, pady=5, sticky='e')  # Фамилия
    global lastname_entry
    lastname_entry = ctk.CTkEntry(app)  # Поле для фамилии
    lastname_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(app, text="Subject").grid(row=2, column=0, padx=5, pady=5, sticky='e')
    global subject_option_menu
    subject_option_menu = ctk.CTkOptionMenu(app, values=subjects, command=lambda x: update_student_list())
    subject_option_menu.grid(row=2, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(app, text="Group").grid(row=3, column=0, padx=5, pady=5, sticky='e')
    global group_option_menu
    group_option_menu = ctk.CTkOptionMenu(app, values=groups, command=lambda x: update_student_list())
    group_option_menu.grid(row=3, column=1, padx=5, pady=5, sticky='w')

    ctk.CTkLabel(app, text="Grade").grid(row=4, column=0, padx=5, pady=5, sticky='e')
    global grade_option_menu
    grade_option_menu = ctk.CTkOptionMenu(app, values=grades, command=lambda x: update_student_list())
    grade_option_menu.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    add_button = ctk.CTkButton(app, text="Add Student", command=add_student, fg_color="green")
    add_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

    # Вторая колонка
    ctk.CTkLabel(app, text="Delete Student by ID").grid(row=0, column=2, padx=5, pady=5, sticky='e')
    global delete_id_entry
    delete_id_entry = ctk.CTkEntry(app)
    delete_id_entry.grid(row=0, column=3, padx=5, pady=5, sticky='w')

    delete_button = ctk.CTkButton(app, text="Delete Student", command=delete_student, fg_color="red")
    delete_button.grid(row=1, column=2, columnspan=2, padx=5, pady=10)

    # Третья колонка
    ctk.CTkButton(app, text="Sort by Name", command=lambda: sort_students('name')).grid(row=0, column=4, padx=5, pady=5)
    ctk.CTkButton(app, text="Sort by Last Name", command=lambda: sort_students('lastname')).grid(row=1, column=4, padx=5, pady=5)  # Сортировка по фамилии
    ctk.CTkButton(app, text="Sort by Grade", command=lambda: sort_students('grade')).grid(row=2, column=4, padx=5, pady=5)

    # Список студентов
    global student_list_frame
    student_list_frame = ctk.CTkScrollableFrame(app)
    student_list_frame.grid(row=6, column=0, columnspan=5, pady=10, sticky='nsew')

    update_student_list()  # Заполнение списка студентов
    app.mainloop()

if __name__ == "__main__":
    main()