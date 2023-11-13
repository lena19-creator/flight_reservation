import tkinter as tk
from tkinter import messagebox
import pymysql

import subprocess
import platform
import runpy

def verify_login(email, password):
    # Connectez-vous à la base de données
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='air_reservation',
        port=8889
    )
    try:
        # Créez un curseur et exécutez la requête SQL pour trouver l'utilisateur
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE email = %s AND password = %s", (email, password))
            result = cursor.fetchone()
            return result is not None  # Si result n'est pas None, l'utilisateur existe
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur de base de données: {e}")
        return False
    finally:
        conn.close()

def login():
    email = email_entry.get()
    password = password_entry.get()

    # Vérifiez les identifiants de l'utilisateur
    if verify_login(email, password):
        # Fermez la fenêtre de connexion
        root.destroy()

        #runpy.run_path(path_name='Page_Principale.py')
        try:
            if platform.system() == 'Windows':
                subprocess.Popen(["python", "homepage.py"], shell=True)
            else:
                subprocess.Popen(["python3", "homepage.py"])
        except Exception as e:
            messagebox.showerror("Error", f"error when you want to redirect the page : {e}")
    else:
        # Affichez un message d'erreur si les identifiants sont invalides
        error_label.config(text=" incorrect email or password !", fg="red")

# Créez la fenêtre principale
root = tk.Tk()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.configure(bg='yellow')
root.title("Connexion")

# Créez un cadre pour le formulaire de connexion
login_frame = tk.Frame(root)
login_frame.pack(pady=20)

# Créez et placez les widgets pour l'email
email_label = tk.Label(login_frame, text="Email")
email_label.grid(row=0, column=0, padx=10, pady=10)
email_entry = tk.Entry(login_frame)
email_entry.grid(row=0, column=1, padx=10, pady=10)

# Créez et placez les widgets pour le mot de passe
password_label = tk.Label(login_frame, text="password")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Créez et placez le bouton de connexion
login_button = tk.Button(login_frame, text="Connection", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Créez et placez le label pour les messages d'erreur
error_label = tk.Label(root, text="")
error_label.pack()

# Lancez la boucle principale de l'application
root.mainloop()


