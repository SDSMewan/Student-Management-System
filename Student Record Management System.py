import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

# ==========================================
# DATA STRUCTURES (Assignment Requirement)
# ==========================================
HEADERS = ("Student ID", "Student Name", "Email", "Age", "Gender",
           "Mobile Number", "Address", "Batch")  # Tuple with 8 fields
student_ids = set()  # Set
student_records = {}  # Dictionary
student_list = []  # List

FILE_NAME = "student_data.csv"


# ==========================================
# USER-DEFINED FUNCTIONS
# ==========================================
def load_data():
    if not os.path.exists(FILE_NAME):
        return
    try:
        with open(FILE_NAME, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) == 8:  # Updated to 8 fields
                    s_id, name, email, age, gender, mobile, address, batch = row
                    student_ids.add(s_id)
                    student_records[s_id] = {
                        "name": name,
                        "email": email,
                        "age": age,
                        "gender": gender,
                        "Mobile Number": mobile,
                        "Address": address,
                        "Batch": batch,
                    }
                    student_list.append(row)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not load data: {e}")


def save_data():
    try:
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(HEADERS)
            for s_id, details in student_records.items():
                writer.writerow([
                    s_id,
                    details["name"],
                    details["email"],
                    details["age"],
                    details["gender"],
                    details["Mobile Number"],
                    details["Address"],
                    details["Batch"]
                ])
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save data: {e}")


def refresh_table():
    for item in tree.get_children():
        tree.delete(item)
    for s_id, details in student_records.items():
        tree.insert("", "end", values=(
            s_id,
            details["name"],
            details["email"],
            details["age"],
            details["gender"],
            details["Mobile Number"],
            details["Address"],
            details["Batch"]
        ))


def clear_fields():
    entry_id.config(state=tk.NORMAL)
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_gender.delete(0, tk.END)
    entry_mobile.delete(0, tk.END)
    entry_address.delete(0, tk.END)
    entry_batch.delete(0, tk.END)


def add_student():
    s_id = entry_id.get().strip()
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    age = entry_age.get().strip()
    gender = entry_gender.get().strip()
    mobile = entry_mobile.get().strip()
    address = entry_address.get().strip()
    batch = entry_batch.get().strip()

    # Check all fields are filled
    if not all([s_id, name, email, age, gender, mobile, address, batch]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    if s_id in student_ids:
        messagebox.showerror("Duplicate Error", f"Student ID '{s_id}' already exists! Use Update instead.")
        return

    # Validate age is a positive number
    try:
        age_int = int(age)
        if age_int <= 0 or age_int > 75:
            messagebox.showerror("Value Error", "Age must be between 1 and 75.")
            return
    except ValueError:
        messagebox.showerror("Type Error", "Age must be a valid number!")
        return

    # Validate email format (basic check)
    if "@" not in email or "." not in email:
        messagebox.showerror("Format Error", "Please enter a valid email address!")
        return

    student_ids.add(s_id)
    student_records[s_id] = {
        "name": name,
        "email": email,
        "age": str(age),
        "gender": gender,
        "Mobile Number": mobile,
        "Address": address,
        "Batch": batch
    }

    save_data()
    refresh_table()
    clear_fields()
    messagebox.showinfo("Success", "Student added successfully!")


def on_tree_select(event):
    """Fills the entry fields when a row in the Treeview is clicked."""
    selected_item = tree.selection()
    if not selected_item:
        return

    item = tree.item(selected_item)
    record = item['values']

    clear_fields()

    # Populate fields (order matches HEADERS)
    entry_id.insert(0, record[0])
    entry_id.config(state=tk.DISABLED)
    entry_name.insert(0, record[1])
    entry_email.insert(0, record[2])
    entry_age.insert(0, record[3])
    entry_gender.insert(0, record[4])
    entry_mobile.insert(0, record[5])
    entry_address.insert(0, record[6])
    entry_batch.insert(0, record[7])


def update_student():
    """Updates the selected student's record."""
    s_id = entry_id.get().strip()
    name = entry_name.get().strip()
    email = entry_email.get().strip()
    age = entry_age.get().strip()
    gender = entry_gender.get().strip()
    mobile = entry_mobile.get().strip()
    address = entry_address.get().strip()
    batch = entry_batch.get().strip()

    if not s_id:
        messagebox.showerror("Error", "Please select a student from the table to update.")
        return

    if s_id not in student_ids:
        messagebox.showerror("Error", "Student ID not found!")
        return

    # Check all fields are filled
    if not all([name, email, age, gender, mobile, address, batch]):
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    # Validate age
    try:
        age_int = int(age)
        if age_int <= 0 or age_int > 150:
            messagebox.showerror("Value Error", "Age must be between 1 and 150.")
            return
    except ValueError:
        messagebox.showerror("Type Error", "Age must be a valid number!")
        return

    # Validate email
    if "@" not in email or "." not in email:
        messagebox.showerror("Format Error", "Please enter a valid email address!")
        return

    # Update Dictionary
    student_records[s_id] = {
        "name": name,
        "email": email,
        "age": str(age),
        "gender": gender,
        "Mobile Number": mobile,
        "Address": address,
        "Batch": batch
    }

    save_data()
    refresh_table()
    clear_fields()
    entry_id.config(state=tk.NORMAL)
    messagebox.showinfo("Success", "Student record updated successfully!")


def delete_student():
    """Deletes the selected student record."""
    s_id = entry_id.get().strip()

    if not s_id:
        messagebox.showerror("Error", "Please select a student from the table to delete.")
        return

    if s_id not in student_ids:
        messagebox.showerror("Error", "Student ID not found!")
        return

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {s_id}?")
    if confirm:
        student_ids.remove(s_id)
        del student_records[s_id]

        save_data()
        refresh_table()
        clear_fields()
        entry_id.config(state=tk.NORMAL)
        messagebox.showinfo("Success", "Student deleted successfully!")


def search_student():
    """Searches for a student by ID and displays only their record."""
    search_id = entry_search.get().strip()

    if not search_id:
        messagebox.showwarning("Warning", "Please enter a Student ID to search.")
        return

    if search_id in student_records:
        # Clear table
        for item in tree.get_children():
            tree.delete(item)
        # Insert only the searched student
        details = student_records[search_id]
        tree.insert("", "end", values=(
            search_id,
            details["name"],
            details["email"],
            details["age"],
            details["gender"],
            details["Mobile Number"],
            details["Address"],
            details["Batch"]
        ))
    else:
        messagebox.showinfo("Not Found", f"No student found with ID: {search_id}")


def show_all():
    """Shows all student records in the table."""
    refresh_table()
    entry_search.delete(0, tk.END)


# ==========================================
# GUI SETUP (Tkinter) with Background Colors
# ==========================================
root = tk.Tk()
root.title("Student Record Management System")
root.geometry("1200x700")
root.configure(bg="#2c3e50")  # Dark blue-gray background for root window

# Style configuration
style = ttk.Style()
style.theme_use('clam')

# Configure colors for different elements
style.configure("TLabelframe", background="#34495e", foreground="white", relief="solid")
style.configure("TLabelframe.Label", background="#34495e", foreground="white", font=('Arial', 10, 'bold'))
style.configure("TButton", background="#3498db", foreground="white", borderwidth=1, focusthickness=3)
style.map("TButton", background=[('active', '#2980b9')])
style.configure("TLabel", background="#34495e", foreground="white")
style.configure("TFrame", background="#34495e")

# Main container with background color
main_container = ttk.Frame(root, padding="10")
main_container.configure(style="TFrame")
main_container.pack(fill=tk.BOTH, expand=True)

# Search Frame with custom colors
frame_search = ttk.LabelFrame(main_container, text="Search", padding="10")
frame_search.pack(fill=tk.X, pady=(0, 10))

tk.Label(frame_search, text="Search by ID:", bg="#34495e", fg="white", font=('Arial', 10)).pack(side=tk.LEFT, padx=(0, 5))
entry_search = tk.Entry(frame_search, width=20, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_search.pack(side=tk.LEFT, padx=5)

btn_search = tk.Button(frame_search, text="Search", command=search_student,
                      bg="#3498db", fg="white", font=('Arial', 10, 'bold'),
                      relief=tk.RAISED, bd=2, padx=10, cursor="hand2")
btn_search.pack(side=tk.LEFT, padx=5)

btn_show_all = tk.Button(frame_search, text="Show All", command=show_all,
                        bg="#2ecc71", fg="white", font=('Arial', 10, 'bold'),
                        relief=tk.RAISED, bd=2, padx=10, cursor="hand2")
btn_show_all.pack(side=tk.LEFT, padx=5)

# Input Frame with custom colors
frame_input = ttk.LabelFrame(main_container, text="Student Information", padding="10")
frame_input.pack(fill=tk.X, pady=(0, 10))

# Configure grid columns to have equal weight
frame_input.columnconfigure(1, weight=1)
frame_input.columnconfigure(3, weight=1)

# Left column
tk.Label(frame_input, text="Student ID:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
entry_id = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_id.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

tk.Label(frame_input, text="Student Name:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=1, column=0, sticky=tk.W, pady=5, padx=5)
entry_name = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_name.grid(row=1, column=1, pady=5, padx=5, sticky=tk.W)

tk.Label(frame_input, text="Email:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=2, column=0, sticky=tk.W, pady=5, padx=5)
entry_email = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_email.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

tk.Label(frame_input, text="Age:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=3, column=0, sticky=tk.W, pady=5, padx=5)
entry_age = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_age.grid(row=3, column=1, pady=5, padx=5, sticky=tk.W)

tk.Label(frame_input, text="Gender:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=4, column=0, sticky=tk.W, pady=5, padx=5)
entry_gender = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_gender.grid(row=4, column=1, pady=5, padx=5, sticky=tk.W)

# Right column
tk.Label(frame_input, text="Mobile Number:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=0, column=2, sticky=tk.W, pady=5, padx=5)
entry_mobile = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_mobile.grid(row=0, column=3, pady=5, padx=5, sticky=tk.W)

tk.Label(frame_input, text="Address:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=1, column=2, sticky=tk.W, pady=5, padx=5)
entry_address = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_address.grid(row=1, column=3, pady=5, padx=5, sticky=tk.W)

tk.Label(frame_input, text="Batch:", bg="#34495e", fg="white", font=('Arial', 10)).grid(row=2, column=2, sticky=tk.W, pady=5, padx=5)
entry_batch = tk.Entry(frame_input, width=30, bg="#ecf0f1", fg="#2c3e50", font=('Arial', 10), relief=tk.SOLID, bd=2)
entry_batch.grid(row=2, column=3, pady=5, padx=5, sticky=tk.W)

# Buttons Frame with custom colors
frame_buttons = ttk.Frame(main_container)
frame_buttons.configure(style="TFrame")
frame_buttons.pack(fill=tk.X, pady=(0, 10))

btn_add = tk.Button(frame_buttons, text="Add", command=add_student,
                   bg="#3498db", fg="white", font=('Arial', 11, 'bold'),
                   relief=tk.RAISED, bd=2, padx=15, pady=5, cursor="hand2")
btn_add.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(frame_buttons, text="Update", command=update_student,
                      bg="#f39c12", fg="white", font=('Arial', 11, 'bold'),
                      relief=tk.RAISED, bd=2, padx=15, pady=5, cursor="hand2")
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(frame_buttons, text="Delete", command=delete_student,
                      bg="#e74c3c", fg="white", font=('Arial', 11, 'bold'),
                      relief=tk.RAISED, bd=2, padx=15, pady=5, cursor="hand2")
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(frame_buttons, text="Clear", command=clear_fields,
                     bg="#95a5a6", fg="white", font=('Arial', 11, 'bold'),
                     relief=tk.RAISED, bd=2, padx=15, pady=5, cursor="hand2")
btn_clear.pack(side=tk.LEFT, padx=5)

btn_exit = tk.Button(frame_buttons, text="Exit", command=root.quit,
                    bg="#2c3e50", fg="white", font=('Arial', 11, 'bold'),
                    relief=tk.RAISED, bd=2, padx=15, pady=5, cursor="hand2")
btn_exit.pack(side=tk.RIGHT, padx=5)

# Table Frame with custom colors
frame_table = ttk.LabelFrame(main_container, text="Student Records", padding="10")
frame_table.pack(fill=tk.BOTH, expand=True)

# Table (Treeview) with scrollbar and custom colors
columns = HEADERS
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=15)

# Style for Treeview
style.configure("Treeview", background="#ecf0f1", foreground="#2c3e50", rowheight=25, fieldbackground="#ecf0f1")
style.configure("Treeview.Heading", background="#34495e", foreground="white", relief="solid", font=('Arial', 10, 'bold'))
style.map('Treeview', background=[('selected', '#3498db')])

# Add scrollbars
vsb = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(frame_table, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

# Configure columns with appropriate widths
column_widths = [100, 150, 150, 60, 80, 120, 200, 100]  # Adjusted widths
for i, col in enumerate(columns):
    tree.heading(col, text=col)
    tree.column(col, width=column_widths[i], anchor=tk.CENTER)

# Bind the click event
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Grid layout for tree and scrollbars
tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")

frame_table.grid_rowconfigure(0, weight=1)
frame_table.grid_columnconfigure(0, weight=1)

# ==========================================
# INITIALIZATION
# ==========================================
load_data()
refresh_table()

root.mainloop()
