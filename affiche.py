import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
import subprocess
import platform
import runpy
import ttkthemes
from ttkthemes import ThemedStyle  # Importez la classe ThemedStyle

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

        try:
            if platform.system() == 'Windows':
                subprocess.Popen(["python", "homepage.py"], shell=True)
            else:
                subprocess.Popen(["python3", "homepage.py"])
        except Exception as e:
            messagebox.showerror("Error", f"Erreur lors de la redirection : {e}")
    else:
        # Affichez un message d'erreur si les identifiants sont invalides
        error_label.config(text="Email ou mot de passe incorrect !", fg="red")

# Créez la fenêtre principale
root = tk.Tk()
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.configure(bg='white')
root.title("Connexion")

# Appliquez le thème à la fenêtre principale
style = ThemedStyle(root)
style.set_theme("aquativo")  # Choisissez le thème "aquativo"

# Créez un cadre pour le formulaire de connexion
login_frame = ttk.Frame(root)  # Utilisez ttk.Frame
login_frame.pack(pady=20)

# Créez et placez les widgets pour l'email
email_label = ttk.Label(login_frame, text="Email")  # Utilisez ttk.Label
email_label.grid(row=0, column=0, padx=10, pady=10)
email_entry = ttk.Entry(login_frame)  # Utilisez ttk.Entry
email_entry.grid(row=0, column=1, padx=10, pady=10)

# Créez et placez les widgets pour le mot de passe
password_label = ttk.Label(login_frame, text="Mot de passe")  # Utilisez ttk.Label
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(login_frame, show="*")  # Utilisez ttk.Entry
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Créez et placez le bouton de connexion
login_button = ttk.Button(login_frame, text="Connexion", command=login)  # Utilisez ttk.Button
login_button.grid(row=2, column=0, columnspan=2, pady=10)

# Créez et placez le label pour les messages d'erreur
error_label = ttk.Label(root, text="")
error_label.pack()

# Lancez la boucle principale de l'application
root.mainloop()


