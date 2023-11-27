import tkinter as tk
from tkinter import messagebox

def valider_paiement():
    numero_carte = numero_carte_entry.get()
    date_expiration = date_expiration_entry.get()
    code_secret = code_secret_entry.get()

    if len(numero_carte) < 12 or not numero_carte.isdigit():
        messagebox.showerror("Erreur", "Numéro de carte invalide")
    elif len(date_expiration) != 7 or not date_expiration[2] == '/' or not date_expiration[:2].isdigit() or not date_expiration[3:].isdigit():
        messagebox.showerror("Erreur", "Date d'expiration invalide (Format : MM/AAAA)")
    elif len(code_secret) != 3 or not code_secret.isdigit():
        messagebox.showerror("Erreur", "Code secret invalide")
    else:
        messagebox.showinfo("Paiement réussi", "Paiement réussi !")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Paiement de Vol")

# Création des champs de saisie
numero_carte_label = tk.Label(root, text="Numéro de carte :")
numero_carte_label.pack()
numero_carte_entry = tk.Entry(root)
numero_carte_entry.pack()

date_expiration_label = tk.Label(root, text="Date d'expiration (MM/AAAA) :")
date_expiration_label.pack()
date_expiration_entry = tk.Entry(root)
date_expiration_entry.pack()

code_secret_label = tk.Label(root, text="Code secret (3 chiffres) :")
code_secret_label.pack()
code_secret_entry = tk.Entry(root)
code_secret_entry.pack()

valider_button = tk.Button(root, text="Valider le paiement", command=valider_paiement)
valider_button.pack()

root.mainloop()
