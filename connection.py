import tkinter as tk
from tkinter import font
from tkinter import Tk, Label
import pymysql
from PIL import Image, ImageTk
from customers import CustomerPage
from guest import GuestPage
from employee import EmployeePage


class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System")

        self.is_customer = False
        self.is_employee = False
        self.user_email = None

        # background image
        self.bg_image = tk.PhotoImage(file="avion.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.logo_image = Image.open("logo3.png")
        self.logo_image = self.logo_image.resize((100, 100))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Label creation to display the logo
        self.logo_label = Label(self.root, image=self.logo_photo, bg="#000000")
        self.logo_label.place(x=1320, y=60)


        self.header = tk.Frame(self.root, bg="#FFE4E1")
        self.header.pack(side="top", fill="x")

        button_font = font.Font(size=30)
        self.welcome_button = tk.Button(self.header, text="Welcome", command=self.show_bienvenue, font=button_font)
        self.welcome_button.pack(side="left")

        # creation of the bordure for the form
        self.form_frame = tk.Frame(self.root, bg="#f0f0f0", bd=2)

        self.email_label = tk.Label(self.form_frame, text="Email", bg="#f0f0f0", fg="#333", font=("Arial", 12))
        self.email_label.grid(row=0, column=0, padx=10, pady=5)

        self.txtuserid = tk.Entry(self.form_frame, width=30, font=("Arial", 12))
        self.txtuserid.grid(row=0, column=1, padx=10, pady=5)

        self.password_label = tk.Label(self.form_frame, text="Password", bg="#f0f0f0", fg="#333", font=("Arial", 12))
        self.password_label.grid(row=1, column=0, padx=10, pady=5)

        self.txtpassword = tk.Entry(self.form_frame, show="*", width=30, font=("Arial", 12))
        self.txtpassword.grid(row=1, column=1, padx=10, pady=5)

        self.logme = tk.Button(self.form_frame, text="Log in", font=("Arial", 12), command=self.myclick)
        self.logme.grid(row=2, columnspan=2, pady=10)

        self.create_account_button = tk.Button(self.form_frame, text="Create an account", font=("Arial", 12),
                                               command=self.create_account)
        self.create_account_button.grid(row=3, columnspan=2, pady=5)

        self.enter_guest = tk.Button(self.form_frame, text="Enter as a guest", font=("Arial", 12),
                                     command=self.enter_as_guest)
        self.enter_guest.grid(row=4, columnspan=2, pady=5)

        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.form_frame.pack_forget()

        self.is_form_visible = False

    def show_bienvenue(self):
        if not self.is_form_visible:
            self.form_frame.pack()
            self.is_form_visible = True
        else:
            self.form_frame.pack_forget()
            self.is_form_visible = False

    def myclick(self):
        email = self.txtuserid.get()
        password = self.txtpassword.get()

        # connexion to the data base
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='air_reservation',
            port=8889
        )
        cursor = conn.cursor()

        # Verification for customers
        select_customer_query = "SELECT * FROM customers WHERE email = %s AND password = %s"
        customer_values = (email, password)

        cursor.execute(select_customer_query, customer_values)
        customer_data = cursor.fetchone()

        # Verification for employees
        select_employee_query = "SELECT * FROM employee WHERE email = %s AND password = %s"
        employee_values = (email, password)

        cursor.execute(select_employee_query, employee_values)
        employee_data = cursor.fetchone()

        if customer_data:
            self.is_customer = True
            self.user_email = email  # Stock user email in self.user_email
            self.root.destroy()  # close actual windows

            customer_root = tk.Tk()
            customer_app = CustomerPage(customer_root, self.user_email)
            customer_root.mainloop()
        elif employee_data:
            self.is_employee = True
            self.root.destroy()  # close actual windows

        else:
            print("Invalid login credentials")

        cursor.close()
        conn.close()

        # Redirection
        if self.is_customer:
            customer_root = tk.Tk()
            customer_app = CustomerPage(customer_root, self.user_email)
            customer_root.mainloop()
        elif self.is_employee:
            employee_root = tk.Tk()
            employee_app = EmployeePage(employee_root)
            employee_root.mainloop()

    def create_account(self):
        def save_to_database_from_input():
            customer_type = customer_type_var.get()
            username = username_entry.get()
            password = password_entry.get()
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            self.save_to_database(customer_type, password, name, email, phone)
            create_account_window.destroy()
            self.show_bienvenue()

        create_account_window = tk.Toplevel(self.root)
        create_account_window.title("Create an Account")

        tk.Label(create_account_window, text="Customer Type:").pack()
        customer_types = ["Regular", "Senior"]
        customer_type_var = tk.StringVar()
        customer_type_var.set(customer_types[0])
        customer_type_menu = tk.OptionMenu(create_account_window, customer_type_var, *customer_types)
        customer_type_menu.pack()

        # Add label

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

        tk.Label(create_account_window, text=":").pack()
        tk.Button(create_account_window, text="Create Account", command=lambda: self.save_to_database_from_input(
            username_entry.get(), password_entry.get(), name_entry.get(), email_entry.get(), phone_entry.get())).pack()

    def save_to_database_from_input(self, username, password, name, email, phone):
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
                print(
                    f"Creating account for {username}, Name: {name}, Email: {email}, Phone: {phone}")  # display a successfull message
        except pymysql.Error as e:
            print(f"Error in database: {e}")  # display error
        finally:
            conn.close()

    def enter_as_guest(self):
        def save_guest_to_database(username):
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password='root',
                db='air_reservation',
                port=8889
            )
            try:
                with conn.cursor() as cursor:
                    # Insertion of the data
                    sql = "INSERT INTO guest (username) VALUES (%s)"
                    cursor.execute(sql, (username,))
                    conn.commit()
                    print(f"Entering as guest: {username}")
            except pymysql.Error as e:
                print(f"Error in database: {e}")
            finally:
                conn.close()

        def enter_guest_clicked():
            username = guest_name_entry.get()
            save_guest_to_database(username)
            guest_window.destroy()

            self.root.destroy()
            guest_root = tk.Tk()
            guest_app = GuestPage(guest_root)
            guest_root.mainloop()

        guest_window = tk.Toplevel(self.root)
        guest_window.title("Enter as a Guest")

        tk.Label(guest_window, text="Username:").pack()
        guest_name_entry = tk.Entry(guest_window)
        guest_name_entry.pack()

        tk.Button(guest_window, text="Enter as a Guest", command=enter_guest_clicked).pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationApp(root)
    root.mainloop()
