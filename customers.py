import tkinter as tk
import pymysql

class CustomerPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Page")

        # Ajouter un cadre pour organiser les widgets
        self.frame = tk.Frame(self.root, bg="#FFFFFF")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Créer une étiquette pour afficher le message de bienvenue
        welcome_label = tk.Label(self.frame, text="Welcome to Customer Page", font=("Arial", 18))
        welcome_label.pack(pady=20)

        # Créer un bouton pour se déconnecter ou fermer la fenêtre
        logout_button = tk.Button(self.frame, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

    def logout(self):
        # Fermer la fenêtre de la page client lorsqu'on se déconnecte
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerPage(root)
    root.mainloop()


