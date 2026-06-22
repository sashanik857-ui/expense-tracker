import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

expenses = []


def save_data():
with open("expenses.json", "w", encoding="utf-8") as file:
json.dump(expenses, file, ensure_ascii=False, indent=4)


def load_data():
global expenses

if os.path.exists("expenses.json"):
with open("expenses.json", "r", encoding="utf-8") as file:
expenses = json.load(file)

for expense in expenses:
table.insert(
"",
tk.END,
values=(
expense["amount"],
expense["category"],
expense["date"]
)
)


def add_expense():
amount = amount_entry.get()
category = category_entry.get()
date = date_entry.get()

try:
amount = float(amount)
if amount <= 0:
raise ValueError
except ValueError:
messagebox.showerror(
"Ошибка",
"Сумма должна быть положительным числом."
)
return

try:
datetime.strptime(date, "%Y-%m-%d")
except ValueError:
messagebox.showerror(
"Ошибка",
"Введите дату в формате ГГГГ-ММ-ДД."
)
return

expense = {
"amount": amount,
"category": category,
"date": date
}

expenses.append(expense)

table.insert(
"",
tk.END,
values=(amount, category, date)
)

save_data()

amount_entry.delete(0, tk.END)
category_entry.delete(0, tk.END)
date_entry.delete(0, tk.END)


def calculate_total():
total = sum(item["amount"] for item in expenses)
total_label.config(text=f"Общая сумма: {total}")


def filter_category():
category = filter_entry.get().lower()

for item in table.get_children():
table.delete(item)

for expense in expenses:
if category in expense["category"].lower():
table.insert(
"",
tk.END,
values=(
expense["amount"],
expense["category"],
expense["date"]
)
)


window = tk.Tk()
window.title("Expense Tracker")
window.geometry("700x500")

tk.Label(window, text="Сумма").pack()
amount_entry = tk.Entry(window)
amount_entry.pack()

tk.Label(window, text="Категория").pack()
category_entry = tk.Entry(window)
category_entry.pack()

tk.Label(window, text="Дата (ГГГГ-ММ-ДД)").pack()
date_entry = tk.Entry(window)
date_entry.pack()

tk.Button(
window,
text="Добавить расход",
command=add_expense
).pack(pady=10)

columns = ("Сумма", "Категория", "Дата")

table = ttk.Treeview(
window,
columns=columns,
show="headings"
)

for col in columns:
table.heading(col, text=col)

table.pack(fill="both", expand=True)

tk.Button(
window,
text="Подсчитать сумму",
command=calculate_total
).pack()

total_label = tk.Label(window, text="Общая сумма: 0")
total_label.pack()

tk.Label(window, text="Фильтр по категории").pack()

filter_entry = tk.Entry(window)
filter_entry.pack()

tk.Button(
window,
text="Фильтровать",
command=filter_category
).pack()

load_data()

window.mainloop()
