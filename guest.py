import tkinter as tk
from tkinter import Label, Frame , Button
from PIL import Image, ImageTk

import subprocess


class GuestPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to your Guest Page")


        # Charger l'image de fond
        self.bg_image = Image.open("image4.png")
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


        self.add_buttons()

    def add_buttons(self):
        button_frame = Frame(self.root, bg="white", bd=3)
        button_frame.place(relx=0.5, rely=0.6, anchor="center")


        search_flight_button = Button(button_frame, text="Research a Flight", command=self.search_flight,
                                      font=("Arial", 12), bg="#2196F3", fg="black",activeforeground="white", padx=10, pady=5)
        search_flight_button.pack(pady=10)


    def search_flight(self):

        subprocess.Popen(["python", "researchguest.py"])




if __name__ == "__main__":
    root = tk.Tk()
    app = GuestPage(root)
    root.mainloop()