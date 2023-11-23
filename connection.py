import tkinter as tk
from tkinter import font
import pymysql
from PIL import Image, ImageTk

class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Reservation System")

        # Charger l'image de fond
        self.bg_image = tk.PhotoImage(file="avion.png")
        self.bg_label = tk.Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # En-tête avec un bouton "Bienvenue"
        self.header = tk.Frame(self.root, bg="#FFC0CB")
        self.header.pack(side="top", fill="x")

        button_font = font.Font(size=14)
        self.welcome_button = tk.Button(self.header, text="Bienvenue", command=self.show_bienvenue, font=button_font)
        self.welcome_button.pack(side="left")

        # Créer un cadre pour le formulaire
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

        self.create_account_button = tk.Button(self.form_frame, text="Create an account", font=("Arial", 12), command=self.create_account)
        self.create_account_button.grid(row=3, columnspan=2, pady=5)

        self.enter_guest = tk.Button(self.form_frame, text="Enter as a guest", font=("Arial", 12), command=self.enter_as_guest)
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

        # Connexion à la base de données MySQL
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='air_reservation',
            port=8889
        )
        cursor = conn.cursor()

        select_query = "SELECT * FROM users WHERE email = %s AND password = %s"
        values = (email, password)

        cursor.execute(select_query, values)
        user_data = cursor.fetchone()

        if user_data:
            print("Login successful!")
            # Actions à effectuer après une connexion réussie
        else:
            print("Invalid login credentials")

        cursor.close()
        conn.close()

    def create_account(self):
        def save_to_database_from_input():
            username = username_entry.get()
            password = password_entry.get()
            name = name_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()
            self.save_to_database(username, password, name, email, phone)
            create_account_window.destroy()

        create_account_window = tk.Toplevel(self.root)
        create_account_window.title("Create an Account")

        # Ajouter des labels pour chaque champ
        tk.Label(create_account_window, text="Customer Type:").pack()
        username_entry = tk.Entry(create_account_window)
        username_entry.pack()

        tk.Label(create_account_window, text="Username:").pack()
        password_entry = tk.Entry(create_account_window, show="*")
        password_entry.pack()

        tk.Label(create_account_window, text="Password:").pack()
        name_entry = tk.Entry(create_account_window)
        name_entry.pack()

        tk.Label(create_account_window, text="Name:").pack()
        email_entry = tk.Entry(create_account_window)
        email_entry.pack()

        tk.Label(create_account_window, text="Email:").pack()
        phone_entry = tk.Entry(create_account_window)
        phone_entry.pack()

        tk.Label(create_account_window, text="Phone:").pack()
        tk.Button(create_account_window, text="Create Account", command=lambda: self.save_to_database_from_input(
            username_entry.get(), password_entry.get(), name_entry.get(), email_entry.get(), phone_entry.get())).pack()


    def save_to_database(self, username, password, name, email, phone):
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
                print(f"Creating account for {username}, Name: {name}, Email: {email}, Phone: {phone}")  # Affiche un message de réussite dans la console
        except pymysql.Error as e:
            print(f"Error in database: {e}")  # Affiche l'erreur dans la console en cas d'échec
        finally:
            conn.close()

    def enter_as_guest(self):
        def save_guest_to_database():
            guest_name = guest_name_entry.get()
            self.save_guest_to_db(guest_name)
            guest_window.destroy()

        guest_window = tk.Toplevel(self.root)
        guest_window.title("Enter as a Guest")

        tk.Label(guest_window, text="Username:").pack()
        guest_name_entry = tk.Entry(guest_window)
        guest_name_entry.pack()

        tk.Button(guest_window, text="Enter as a Guest", command=lambda: self.save_guest_to_database(
            guest_name_entry.get())).pack()

    def save_guest_to_db(self, guest_name):
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='air_reservation',
            port=8889
        )
        try:
            with conn.cursor() as cursor:
                # Insertion des données dans la table guest
                sql = "INSERT INTO guest (username) VALUES (%s)"
                cursor.execute(sql, (guest_name,))
                conn.commit()
                print(f"Entering as guest: {guest_name}")  # Message de réussite
        except pymysql.Error as e:
            print(f"Error in database: {e}")  # Affiche l'erreur en cas d'échec
        finally:
            conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationApp(root)
    root.mainloop()


