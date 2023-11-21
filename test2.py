import tkinter as tk

root = tk.Tk()
root.title("Fenêtre avec image en fond")

# Chargement de l'image en tant que fond d'écran
image_path = "de1.png"  # Mettez ici le chemin de votre image
if image_path:
    try:
        # Créer un canvas de la taille de la fenêtre
        canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
        canvas.pack()

        # Charger l'image et la mettre en tant que fond sur le canvas
        background_image = tk.PhotoImage(file=image_path)
        canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

        # Vous pouvez ajouter d'autres éléments à cette fenêtre
        label = tk.Label(root, text="Votre contenu ici", fg="white", font=("Arial", 24))
        label.pack(padx=20, pady=20)

    except FileNotFoundError:
        print("Fichier image introuvable.")
else:
    print("Chemin de l'image non spécifié.")

root.mainloop()
