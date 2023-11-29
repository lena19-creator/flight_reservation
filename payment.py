import tkinter as tk
from tkinter import messagebox
import pymysql
from customers import CustomerPage

def valider_paiement():
    numero_carte = numero_carte_entry.get()
    date_expiration = date_expiration_entry.get()
    code_secret = code_secret_entry.get()

    if len(numero_carte) < 12 or not numero_carte.isdigit():
        messagebox.showerror("Error", "INVALID NUMBER OF CARD")
    elif len(date_expiration) != 7 or not date_expiration[2] == '/' or not date_expiration[:2].isdigit() or not date_expiration[3:].isdigit():
        messagebox.showerror("Error", "INVALID DATE (Format : MM/AAAA)")
    elif len(code_secret) != 3 or not code_secret.isdigit():
        messagebox.showerror("Error", "INVALID SECRET CODE")
    else:
        messagebox.showinfo("Payment sucessfull", "Payment succesfull !")
    paiement_valide = True


# Création de la fenêtre principale
root = tk.Tk()
root.title("flight payment")

# Création des champs de saisie
numero_carte_label = tk.Label(root, text="card number :")
numero_carte_label.pack()
numero_carte_entry = tk.Entry(root)
numero_carte_entry.pack()

date_expiration_label = tk.Label(root, text="Expiration Date (MM/AAAA) :")
date_expiration_label.pack()
date_expiration_entry = tk.Entry(root)
date_expiration_entry.pack()

code_secret_label = tk.Label(root, text="Secret code (3 numbers ) :")
code_secret_label.pack()
code_secret_entry = tk.Entry(root)
code_secret_entry.pack()

valider_button = tk.Button(root, text="Validate payment", command=valider_paiement)
valider_button.pack()



root.mainloop()
