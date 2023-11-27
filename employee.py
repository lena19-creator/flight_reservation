import tkinter as tk
from tkinter import Label, Frame, Button
from PIL import Image, ImageTk
import pymysql

class EmployeePage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to your Employee Page")

        # Charger l'image de fond
        self.bg_image = Image.open("image3.png")
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

        # Récupérer la largeur de la fenêtre principale
        window_width = self.root.winfo_width()

        # Bouton "Modify Flight"
        self.modify_flight_button = Button(self.root, text="Modify Flight", command=self.modify_flight)
        self.modify_flight_button.place(x=(window_width - self.modify_flight_button.winfo_width()) / 2, y=50)

        # Bouton "Discount"
        self.discount_button = Button(self.root, text="Discount", command=self.apply_discount)
        self.discount_button.place(x=(window_width - self.discount_button.winfo_width()) / 2, y=100)

        # Bouton "Sales Analysis"
        self.sales_analysis_button = Button(self.root, text="Sales Analysis", command=self.sales_analysis)
        self.sales_analysis_button.place(x=(window_width - self.sales_analysis_button.winfo_width()) / 2, y=150)

    def modify_flight(self):
        # Ajouter ici le code pour la fonctionnalité "Modify Flight"
        pass

    def apply_discount(self):
        # Ajouter ici le code pour la fonctionnalité "Discount"
        pass

    def sales_analysis(self):
        # Ajouter ici le code pour la fonctionnalité "Sales Analysis"
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeePage(root)
    root.mainloop()
