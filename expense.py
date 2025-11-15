# expenses_tracker_gui
import json
import os
from tkinter import *
from tkinter import messagebox
from datetime import datetime

FILE_NAME = "expenses.json"


# ---------------------- Load & Save Functions ---------------------- #

def load_expenses():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_expenses(expenses):
    with open(FILE_NAME, "w") as f:
        json.dump(expenses, f, indent=4)


# ---------------------- Add Expense ---------------------- #

def add_expense():
    amount = amount_entry.get().strip()
    category = category_entry.get().strip()

    if not amount or not category:
        messagebox.showwarning("Missing Input", "Please fill all fields.")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.")
        return

    date = datetime.now().strftime("%Y-%m-%d")

    expense = {"amount": amount, "category": category, "date": date}
    expenses.append(expense)
    save_expenses(expenses)

    update_listbox()
    amount_entry.delete(0, END)
    category_entry.delete(0, END)
    messagebox.showinfo("Success", "Expense Added!")


# ---------------------- Update Display ---------------------- #

def update_listbox():
    listbox.delete(0, END)
    for i, exp in enumerate(expenses, start=1):
        line = f"{i}. ₦{exp['amount']} - {exp['category']} - {exp['date']}"
        listbox.insert(END, line)


# ---------------------- Total Amount ---------------------- #

def show_total():
    total = sum(exp["amount"] for exp in expenses)
    messagebox.showinfo("Total", f"Total Spent: ₦{total}")


# ---------------------- Delete Expense ---------------------- #

def delete_expense():
    selected = listbox.curselection()
    if not selected:
        messagebox.showwarning("No Selection", "Select an expense to delete.")
        return

    index = selected[0]
    del expenses[index]
    save_expenses(expenses)
    update_listbox()
    messagebox.showinfo("Deleted", "Expense removed.")


# ---------------------- GUI Setup ---------------------- #

root = Tk()
root.title("Expense Tracker")
root.geometry("430x500")
root.resizable(False, False)

# Inputs
Label(root, text="Amount (₦):", font=("Arial", 12)).pack()
amount_entry = Entry(root, font=("Arial", 12))
amount_entry.pack()

Label(root, text="Category:", font=("Arial", 12)).pack()
category_entry = Entry(root, font=("Arial", 12))
category_entry.pack()

# Buttons
Button(root, text="Add Expense", font=("Arial", 12), width=18, bg="#4CAF50", fg="white",
       command=add_expense).pack(pady=10)

Button(root, text="Show Total Spent", font=("Arial", 12), width=18, bg="#2196F3", fg="white",
       command=show_total).pack()

Button(root, text="Delete Selected Expense", font=("Arial", 12), width=22, bg="#f44336", fg="white",
       command=delete_expense).pack(pady=10)

# Listbox
Label(root, text="All Expenses:", font=("Arial", 12)).pack()
listbox = Listbox(root, width=50, height=15, font=("Arial", 11))
listbox.pack()

# Load existing expenses
expenses = load_expenses()
update_listbox()

root.mainloop()
