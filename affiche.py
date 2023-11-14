import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

def verify_login(email, password):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )
    try:
        with conn.cursor() as cursor:
            sql = "SELECT * FROM customers WHERE email = %s AND password = %s"
            cursor.execute(sql, (email, password))
            result = cursor.fetchone()
            return result is not None
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error in database: {e}")
        return False
    finally:
        conn.close()

def save_to_database(username, password, name, email, phone):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO customers (customer_type, username, password, name, email, phone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, ('regular', username, password, name, email, phone))
            conn.commit()

            messagebox.showinfo("Success", "Account created successfully!")
    except pymysql.Error as e:
        messagebox.showerror("Error", f"Error in database: {e}")
    finally:
        conn.close()

def save_guest_to_database(guest_name):
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO guest (username) VALUES (%s)"
            cursor.execute(sql, (guest_name,))
            conn.commit()
            print("Guest added successfully!")
    except pymysql.Error as e:
        print(f"Error in database: {e}")
    finally:
        conn.close()

def create_account():
    def save_to_database_from_input():
        username = username_entry.get()
        password = password_entry.get()
        name = name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        save_to_database(username, password, name, email, phone)

    create_account_window = tk.Toplevel(root)
    create_account_window.title("Create an Account")

    tk.Label(create_account_window, text="Username:").pack()
    username_entry = tk.Entry(create_account_window)
    username_entry.pack()

    tk.Label(create_account_window, text="Password:").pack()
    password_entry = tk.Entry(create_account_window, show="*")
    password_entry.pack()

    tk.Label(create_account_window, text="Name:").pack()
    name_entry = tk.Entry(create_account_window)
    name_entry.pack()

    tk.Label(create_account_window, text="Email:").pack()
    email_entry = tk.Entry(create_account_window)
    email_entry.pack()

    tk.Label(create_account_window, text="Phone:").pack()
    phone_entry = tk.Entry(create_account_window)
    phone_entry.pack()

    tk.Button(create_account_window, text="Create Account", command=save_to_database_from_input).pack()

def enter_as_guest():
    def save_guest_to_database():
        guest_name = guest_name_entry.get()
        save_guest_to_database(guest_name)

    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )

    guest_window = tk.Toplevel(root)
    guest_window.title("Enter as a Guest")

    tk.Label(guest_window, text="Guest Name:").pack()
    guest_name_entry = tk.Entry(guest_window)
    guest_name_entry.pack()

    tk.Button(guest_window, text="Enter as a Guest", command=save_guest_to_database).pack()

def login():
    email = email_entry.get()
    password = password_entry.get()

    if verify_login(email, password):
        # Votre code pour rediriger l'utilisateur vers une autre page
        pass
    else:
        error_label.config(text="Email or password incorrect!", fg="red")

root = tk.Tk()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.configure(bg='white')
root.title("Connexion")

login_frame = ttk.Frame(root)
login_frame.pack(pady=20)

email_label = ttk.Label(login_frame, text="Email")
email_label.grid(row=0, column=0, padx=10, pady=10)
email_entry = ttk.Entry(login_frame)
email_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ttk.Label(login_frame, text="Password")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = ttk.Button(login_frame, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

error_label = ttk.Label(root, text="")
error_label.pack()

tk.Button(root, text="Create Account", command=create_account).pack(pady=10)
tk.Button(root, text="Enter as a Guest", command=enter_as_guest).pack(pady=10)

root.mainloop()

