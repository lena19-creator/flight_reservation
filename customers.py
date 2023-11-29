import tkinter as tk
from tkinter import Label, Frame , Button
from PIL import Image, ImageTk
import pymysql
from tkinter import messagebox
import subprocess

class CustomerPage:
    def __init__(self, root, user_email):
        self.root = root
        self.root.title("Welcome to your Customer Page")
        self.user_email = user_email
        self.user_details = None  # Initialiser user_details comme None

        # Charger l'image de fond
        self.bg_image = Image.open("image2.png")
        self.bg_image = self.bg_image.resize((1200, 800))  # Redimensionner l'image
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.logo_image = Image.open("logo3.png")
        self.logo_image = self.logo_image.resize((100, 100))  # Redimensionner le logo
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Créer un label pour afficher le logo au-dessus de la barre rose
        self.logo_label = Label(self.root, image=self.logo_photo, bg="#000000")
        self.logo_label.place(x=1320, y=60)

        # Créer un cadre pour afficher les détails de la personne connectée
        self.details_frame = Frame(self.root, bg="#FFFFFF")
        self.details_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.add_buttons()


    def add_buttons(self):
        button_frame = Frame(self.root, bg="white", bd=3)
        button_frame.place(relx=0.5, rely=0.6, anchor="center")

        info_button = Button(button_frame, text="Information of the Customer", command=self.show_customer_info,
                             font=("Arial", 12), bg="#4CAF50", fg="black", activeforeground="white", padx=10, pady=5)
        info_button.pack(pady=10)

        search_flight_button = Button(button_frame, text="Research a Flight", command=self.search_flight,
                                      font=("Arial", 12), bg="#2196F3", fg="black",activeforeground="white", padx=10, pady=5)
        search_flight_button.pack(pady=10)

        flight_history_button = Button(button_frame, text="My Flight History", command=self.show_flight_history,
                                       font=("Arial", 12), bg="#f44336", fg="black",activeforeground="white", padx=10, pady=5)
        flight_history_button.pack(pady=10)



    def get_user_details(self):
        # Connectez-vous à la base de données et récupérez les détails de l'utilisateur
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            db='air_reservation',
            port=8889
        )
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        select_query = "SELECT * FROM customers WHERE email = %s"
        cursor.execute(select_query, (self.user_email,))  # Utiliser l'email stocké
        user_data = cursor.fetchone()

        cursor.close()
        conn.close()

        return user_data

    def show_customer_info(self):
        if not self.user_details:
            # Récupérer les détails du client
            self.user_details = self.get_user_details()

            # Afficher les détails dans le cadre
            if self.user_details:
                email_label = Label(self.details_frame, text=f"Email: {self.user_details['email']}", font=("Arial", 12))
                email_label.pack()

                username_label = Label(self.details_frame, text=f"Username: {self.user_details['username']}",
                                       font=("Arial", 12))
                username_label.pack()

                name_label = Label(self.details_frame, text=f"Name: {self.user_details['name']}", font=("Arial", 12))
                name_label.pack()

                phone_label = Label(self.details_frame, text=f"Phone: {self.user_details['phone']}", font=("Arial", 12))
                phone_label.pack()

                customer_type_label = Label(self.details_frame,
                                            text=f"Customer Type: {self.user_details['customer_type']}",
                                            font=("Arial", 12))
                customer_type_label.pack()
            else:
                error_label = Label(self.details_frame, text="Error!", font=("Arial", 12))
                error_label.pack()

        else:
            # Afficher une boîte de dialogue si les détails ont déjà été récupérés
            info_message = f"Email: {self.user_details['email']}\nUsername: {self.user_details['username']}\nName: {self.user_details['name']}\nPhone: {self.user_details['phone']}\nCustomer Type: {self.user_details['customer_type']}"
            messagebox.showinfo("Customer Information", info_message)

    def show_flight_history(self):
        subprocess.Popen(["python", "history.py"])

    def search_flight(self):
        # Lancer le script research.py en tant que processus distinct
        subprocess.Popen(["python", "research.py"])




if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerPage(root)
    root.mainloop()
